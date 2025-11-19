from django.shortcuts import render, get_object_or_404
from .models import Decor, Venue , VenueReservation
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from EventApp.models import Event
from .forms import ReservationForm
from django.core.exceptions import ValidationError

def decor_detail(request, decor_id):
    decor = get_object_or_404(
        Decor.objects.prefetch_related('venues'),  # venues = related_name on Venue.decor
        pk=decor_id
    )
    return render(request, 'venues/decor_detail.html', {'decor': decor})



def index(request):
    return render(request, 'index.html')  # lit ProjetWeb/templates/index.html
from .forms import ReservationForm   # garde bien cet import en haut du fichier

def venues_list(request):
    venues = Venue.objects.select_related("decor").all()
    # Filter events associated with the logged-in user
    events = Event.objects.filter(user=request.user).order_by("-created_at")

    # 🔹 Créer une instance du formulaire pour le modal
    reservation_form = ReservationForm()

    return render(
        request,
        "venues/venues_list.html",
        {
            "venues": venues,
            "events": events,
            "reservation_form": reservation_form,  # 🔥 très important
        },
    )

# VenuesApp/views.py

# VenuesApp/views.py
@login_required

@login_required
def reserve_venue(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    events = Event.objects.filter(user=request.user)
    if request.method == 'POST':
        event_id = request.POST.get('event')

        # Ensure the event belongs to the logged-in user
        try:
            event = Event.objects.get(pk=event_id, user=request.user)
        except Event.DoesNotExist:
            messages.error(request, "Event not found or not associated with your account.")
            return redirect('venues_list')

        # Get the reservation start time and duration
        start_time_str = request.POST.get('start_time')
        duration_minutes = int(request.POST.get('duration_minutes'))

        # Convert the start time to datetime
        try:
            start_datetime = datetime.strptime(start_time_str, '%H:%M')
        except ValueError:
            messages.error(request, "Invalid start time format.")
            return redirect('venues_list')

        # Calculate end time based on start time and duration
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)

        # Check for overlapping reservations for the same venue and date
        overlapping_reservations = VenueReservation.objects.filter(
            venue=venue,
            date_reservation=event.date_evenement  # Ensure it's the same date
        )

        for reservation in overlapping_reservations:
            reservation_start = datetime.combine(reservation.date_reservation, reservation.start_time)
            reservation_end = reservation_start + timedelta(minutes=reservation.duration_minutes)
            
            # Check if the new reservation's time overlaps with any existing one
            if (start_datetime < reservation_end and end_datetime > reservation_start):
                messages.error(request, "This venue is already reserved during the requested time.")
                return redirect('venues_list')

        # Check if the event already has a reservation
        existing_event_reservation = VenueReservation.objects.filter(
            event_id=event_id
        )
        
        if existing_event_reservation.exists():
            messages.error(request, "This event already has a reservation.")
            return redirect('venues_list')

        # Create the reservation instance
        reservation = VenueReservation(
            venue=venue,
            event=event,
            user=request.user,  # Set the user to the currently logged-in user
            date_reservation=event.date_evenement,  # Set the reservation date to the event date
            start_time=start_datetime,  # Set the start time of the reservation
            duration_minutes=duration_minutes  # Set the duration of the reservation
        )

        # Call clean() to validate overlapping reservations before saving
        try:
            reservation.clean()  # This will raise ValidationError if there's an overlap
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('venues_list')

        # Save the reservation
        reservation.save()

        messages.success(request, "Reservation successfully created!")
        return redirect('venues_list')

    else:
        form = ReservationForm()

    return render(request, 'venues/reserve.html', {'venue': venue, 'form': form})


@login_required
def user_reservations(request):
    # Fetch the reservations for the logged-in user
    reservations = VenueReservation.objects.filter(user=request.user)
    return render(request, 'venues/user_reservations.html', {'reservations': reservations})

