from django.shortcuts import render, redirect, get_object_or_404
from .models import Invitation, Guest
from .forms import InvitationForm, GuestForm
from EventApp.models import Event
from django.http import JsonResponse

def invitation_list(request):
    invitations = Invitation.objects.all()
    return render(request, 'InvitationAPP/invitation_list.html', {'liste': invitations})

def invitation_detail(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    return render(request, 'InvitationAPP/invitation_detail.html', {'invitation': invitation})

def invitation_create(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('InvitationAPP:invitation_list')
    else:
        form = InvitationForm(user=request.user)
    return render(request, 'InvitationAPP/invitation_form.html', {'form': form})

def invitation_update(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if request.method == 'POST':
        form = InvitationForm(request.POST, instance=invitation, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('InvitationAPP:invitation_list')
    else:
        form = InvitationForm(instance=invitation, user=request.user)
    return render(request, 'InvitationAPP/invitation_form.html', {'form': form})

def event_info(request, event_id):
    try:
        e = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'not_found'}, status=404)
    loc = None
    st = None
    try:
        r = getattr(e, 'reservation', None)
        if r and r.venue:
            loc = r.venue.adresse_v or r.venue.nom_v
            st = r.start_time.strftime('%H:%M') if r.start_time else None
    except Exception:
        loc = None
        st = None
    return JsonResponse({
        'start_date': e.date_evenement.isoformat() if e.date_evenement else None,
        'venue_name': r.venue.nom_v if r and r.venue else None,
        'start_time': st,
    })

from django.http import JsonResponse
def invitation_delete(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if request.method == 'POST':
        invitation.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('InvitationAPP:invitation_list')
    return JsonResponse({'error': 'Invalid request'}, status=400)

def guest_list(request, invitation_pk):
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
    guests = Guest.objects.filter(invitation=invitation)
    try:
        print(f"Guest list for invitation {invitation.pk} ({invitation.name}): count={guests.count()}")
    except Exception:
        pass
    return render(request, 'InvitationAPP/guest_list.html', {'invitation': invitation, 'guests': guests})

def guest_create(request, invitation_pk):
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
    if request.method == 'POST':
        form = GuestForm(request.POST)
        # Ensure unique_together (invitation, email) is validated by setting the instance before is_valid()
        form.instance.invitation = invitation
        if form.is_valid():
            guest = form.save()
            return redirect('InvitationAPP:guest_list', invitation_pk=invitation.pk)
    else:
        form = GuestForm()
    return render(request, 'InvitationAPP/guest_form.html', {'form': form, 'invitation': invitation})

def guest_update(request, invitation_pk, pk):
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == 'POST':
        form = GuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return redirect('InvitationAPP:guest_list', invitation_pk=invitation.pk)
    else:
        form = GuestForm(instance=guest)
    return render(request, 'InvitationAPP/guest_form.html', {'form': form, 'invitation': invitation})

def guest_delete(request, invitation_pk, pk):
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == 'POST':
        guest.delete()
        return redirect('InvitationAPP:guest_list', invitation_pk=invitation.pk)
    return render(request, 'InvitationAPP/guest_confirm_delete.html', {'guest': guest, 'invitation': invitation})

def guest_send_options(request, invitation_pk, pk):
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
    guest = get_object_or_404(Guest, pk=pk)
    return render(request, 'InvitationAPP/guest_send_options.html', {'guest': guest, 'invitation': invitation})
