from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .models import Invitation, Guest
from .forms import InvitationForm, GuestForm
from EventApp.models import Event
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage

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

def guest_qr(request, invitation_pk, pk):
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
    guest = get_object_or_404(Guest, pk=pk)
    target_url = request.build_absolute_uri(
        reverse('InvitationAPP:invitation_detail', args=[invitation.pk])
    )
    payload = f"{target_url}?guest={guest.pk}"
    return render(request, 'InvitationAPP/guest_qr.html', {
        'guest': guest,
        'invitation': invitation,
        'qr_payload': payload,
    })

def guest_send_email(request, invitation_pk, pk):
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
    guest = get_object_or_404(Guest, pk=pk)
    sent = False
    error = None
    if guest.email:
        target_url = request.build_absolute_uri(
            reverse('InvitationAPP:invitation_detail', args=[invitation.pk])
        )
        subject = f"Invitation: {invitation.name}"
        body = (
            f"Bonjour {guest.first_name} {guest.last_name},\n\n"
            f"Vous êtes invité à: {invitation.name}.\n"
            f"Date: {invitation.start_date} de {invitation.start_time or ''}\n"
            f"Thème: {invitation.theme}\n\n"
            f"Consultez les détails ici: {target_url}\n\n"
            f"Cordialement."
        )
        try:
            send_mail(subject, body, getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost'), [guest.email])
            sent = True
        except Exception as e:
            error = str(e)
            sent = False
    return render(request, 'InvitationAPP/guest_email_sent.html', {
        'guest': guest,
        'invitation': invitation,
        'sent': sent,
        'error': error,
        'email_backend': getattr(settings, 'EMAIL_BACKEND', ''),
    })

def send_simple_email(request):
    subject = "Hello from Django!"
    message = "This is a test email sent from your Evoria application."
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
    to = request.GET.get('to') or getattr(settings, 'EMAIL_HOST_USER', '')
    recipient_list = [to] if to else []
    if not recipient_list:
        return HttpResponse("No recipient configured. Provide ?to=recipient@example.com or set EMAIL_HOST_USER.", status=400)
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        return HttpResponse(f"Failed: {e}", status=500)
    return HttpResponse("Email sent successfully!")

def send_complex_email(request):
    subject = "Email with HTML and Attachment"
    body = "<p>This is an <strong>HTML email</strong> from Evoria.</p>"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
    to = request.GET.get('to') or getattr(settings, 'EMAIL_HOST_USER', '')
    recipient_list = [to] if to else []
    if not recipient_list:
        return HttpResponse("No recipient configured. Provide ?to=recipient@example.com or set EMAIL_HOST_USER.", status=400)
    try:
        email = EmailMessage(subject, body, from_email, recipient_list)
        email.content_subtype = "html"
        email.send(fail_silently=False)
    except Exception as e:
        return HttpResponse(f"Failed: {e}", status=500)
    return HttpResponse("Complex email sent successfully!")
