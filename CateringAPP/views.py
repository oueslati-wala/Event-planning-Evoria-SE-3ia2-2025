from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Caterer, MenuItem
from .forms import CatererForm, MenuItemForm


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
        return redirect('CateringAPP:caterer_list')
    return render(request, 'CateringAPP/caterer_confirm_delete.html', {'object': caterer})


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
    if selected_id:
        selected = get_object_or_404(Caterer, pk=selected_id)
        items = list(MenuItem.objects.filter(is_available=True, caterer=selected))
    return render(request, 'CateringAPP/front_portal.html', {
        'caterers': caterers,
        'selected': selected,
        'items': items,
    })
