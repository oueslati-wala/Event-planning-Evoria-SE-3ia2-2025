from django.shortcuts import render, get_object_or_404
from .models import Decor, Venue , VenueReservation
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import datetime
from EventApp.models import Event
def decor_detail(request, decor_id):
    decor = get_object_or_404(
        Decor.objects.prefetch_related('venues'),  # venues = related_name on Venue.decor
        pk=decor_id
    )
    return render(request, 'venues/decor_detail.html', {'decor': decor})



def index(request):
    return render(request, 'index.html')  # lit ProjetWeb/templates/index.html
def venues_list(request):
    venues = Venue.objects.select_related("decor").all()
    from EventApp.models import Event
    events = Event.objects.all().order_by("-created_at")
    return render(request, "venues/venues_list.html", {"venues": venues, "events": events})
# VenuesApp/views.py
from .forms import ReservationForm
# VenuesApp/views.py
@login_required
def reserve_venue(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)

    if request.method == 'POST':
        # prefill date from selected event BEFORE validation
        event_id = request.POST.get('event')
        instance_kwargs = {'venue': venue}
        if event_id:
            ev = get_object_or_404(Event, pk=event_id)
            instance_kwargs['date_reservation'] = ev.date_evenement

        instance = VenueReservation(**instance_kwargs)
        form = ReservationForm(request.POST, instance=instance)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user_id = request.user.pk
            if not reservation.date_reservation and reservation.event_id:
                reservation.date_reservation = reservation.event.date_evenement
            if not getattr(reservation, "nom_reservation", None):
                reservation.nom_reservation = f"Réservation {request.user.username}"
            reservation.save()
            messages.success(request, "Réservation enregistrée ✅")
            return redirect('venues_list')
        else:
            print("FORM ERRORS:", form.errors.as_json())
    else:
        form = ReservationForm()

    return render(request, 'venues/reserve.html', {'venue': venue, 'form': form})

