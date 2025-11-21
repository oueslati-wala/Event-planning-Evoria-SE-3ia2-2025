from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from EventApp.models import Event
from .models import Caterer, MenuItem, CateringReservation
from .forms import CatererForm, MenuItemForm, CateringReservationForm


@staff_member_required
def caterer_list(request):
    caterers = Caterer.objects.all()
    return render(request, 'CateringAPP/caterer_list.html', {'liste': caterers})


@staff_member_required
def caterer_create(request):
    if request.method == 'POST':
        form = CatererForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CateringAPP:caterer_list')
    else:
        form = CatererForm()
    return render(request, 'CateringAPP/caterer_form.html', {'form': form})


@staff_member_required
def caterer_update(request, pk):
    caterer = get_object_or_404(Caterer, pk=pk)
    if request.method == 'POST':
        form = CatererForm(request.POST, instance=caterer)
        if form.is_valid():
            form.save()
            return redirect('CateringAPP:caterer_list')
    else:
        form = CatererForm(instance=caterer)
    return render(request, 'CateringAPP/caterer_form.html', {'form': form})


@staff_member_required
def caterer_delete(request, pk):
    caterer = get_object_or_404(Caterer, pk=pk)
    if request.method == 'POST':
        caterer.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('CateringAPP:caterer_list')
    return JsonResponse({'error': 'Invalid request'}, status=400)


def menu_list(request):
    selected_id = request.session.get('selected_caterer_id')
    if not selected_id:
        return redirect('CateringAPP:caterer_choose_list')
    caterer = get_object_or_404(Caterer, pk=selected_id)
    items = MenuItem.objects.filter(is_available=True, caterer=caterer)
    return render(request, 'CateringAPP/menu_list.html', {'items': items, 'caterer': caterer})


def caterer_choose_list(request):
    caterers = Caterer.objects.filter(status='active')
    return render(request, 'CateringAPP/caterer_choose_list.html', {'liste': caterers})


def caterer_choose(request, pk):
    get_object_or_404(Caterer, pk=pk)
    request.session['selected_caterer_id'] = pk
    return redirect('CateringAPP:menu_list')


@staff_member_required
def menu_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CateringAPP:menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'CateringAPP/menu_form.html', {'form': form})


@staff_member_required
def menu_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('CateringAPP:menu_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'CateringAPP/menu_form.html', {'form': form})


@staff_member_required
def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('CateringAPP:menu_list')
    return render(request, 'CateringAPP/menu_confirm_delete.html', {'object': item})


def front_portal(request):
    caterers = Caterer.objects.filter(status='active')
    selected_id = request.GET.get('caterer')
    selected = None
    items = []
    events = Event.objects.filter(user=request.user) if request.user.is_authenticated else []
    if selected_id:
        selected = get_object_or_404(Caterer, pk=selected_id)
        items = list(MenuItem.objects.filter(is_available=True, caterer=selected))
    return render(request, 'CateringAPP/front_portal.html', {
        'caterers': caterers,
        'selected': selected,
        'items': items,
        'events': events,
    })


@login_required
def reserve_catering(request, caterer_id):
    caterer = get_object_or_404(Caterer, pk=caterer_id)
    if request.method == 'POST':
        event_id = request.POST.get('event')
        try:
            event = Event.objects.get(pk=event_id, user=request.user)
        except Event.DoesNotExist:
            messages.error(request, "Événement introuvable ou non associé à votre compte.")
            return redirect('CateringAPP:front_portal')

        start_time_str = request.POST.get('start_time')
        duration_minutes = int(request.POST.get('duration_minutes'))
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, "Format de l'heure de début invalide.")
            return redirect('CateringAPP:front_portal')

        if CateringReservation.objects.filter(event_id=event_id).exists():
            messages.error(request, "Cet événement possède déjà une réservation restauration.")
            return redirect('CateringAPP:front_portal')

        reservation = CateringReservation(
            user=request.user,
            caterer=caterer,
            event=event,
            date_reservation=event.date_evenement,
            start_time=start_time,
            duration_minutes=duration_minutes,
            nom_reservation=f"Restauration – {caterer}"
        )

        try:
            reservation.clean()
        except Exception as e:
            messages.error(request, str(e))
            return redirect('CateringAPP:front_portal')

        reservation.save()
        messages.success(request, "Réservation restauration créée !")
        return redirect('CateringAPP:front_portal')

    return redirect('CateringAPP:front_portal')


@login_required
def my_reservations(request):
    reservations = CateringReservation.objects.filter(user=request.user).select_related('caterer', 'event')
    return render(request, 'CateringAPP/user_reservations.html', {'reservations': reservations})
