from django.shortcuts import render, redirect, get_object_or_404
from .models import Invitation, Guest
from .forms import InvitationForm, GuestForm

def invitation_list(request):
    invitations = Invitation.objects.all()
    return render(request, 'InvitationAPP/invitation_list.html', {'liste': invitations})

def invitation_detail(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    return render(request, 'InvitationAPP/invitation_detail.html', {'invitation': invitation})

def invitation_create(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('InvitationAPP:invitation_list')
    else:
        form = InvitationForm()
    return render(request, 'InvitationAPP/invitation_form.html', {'form': form})

def invitation_update(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if request.method == 'POST':
        form = InvitationForm(request.POST, instance=invitation)
        if form.is_valid():
            form.save()
            return redirect('InvitationAPP:invitation_list')
    else:
        form = InvitationForm(instance=invitation)
    return render(request, 'InvitationAPP/invitation_form.html', {'form': form})

def invitation_delete(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if request.method == 'POST':
        invitation.delete()
        return redirect('InvitationAPP:invitation_list')
    return render(request, 'InvitationAPP/invitation_confirm_delete.html', {'object': invitation})

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
