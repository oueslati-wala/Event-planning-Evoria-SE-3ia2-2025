from django.shortcuts import render, get_object_or_404
from .models import Decor, Venue , VenueReservation
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from EventApp.models import Event
from .forms import ReservationForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import VenueReservation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime


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
    events = Event.objects.filter(user=request.user).order_by("-created_at")
    reservations = VenueReservation.objects.filter(user=request.user)

    # 🔥 ici on passe le user
    reservation_form = ReservationForm(user=request.user)

    today_date = date.today().strftime('%Y-%m-%d')
    today_reservations = reservations.filter(date_reservation=today_date)

    return render(
        request,
        "venues/venues_list.html",
        {
            "venues": venues,
            "events": events,
            "reservation_form": reservation_form,
            "reservations": reservations,
            "today_date": today_date,
            "today_reservations": today_reservations,
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
@require_POST
def edit_reservation(request, reservation_id):
    """
    Modifie une réservation (heure + durée).
    Appelée par le formulaire du popup.
    """
    reservation = get_object_or_404(
        VenueReservation,
        pk=reservation_id,
        user=request.user,  # sécurité : ne modifier que ses propres réservations
    )

    start_time_str = request.POST.get("start_time")
    duration_str = request.POST.get("duration_minutes")

    if not start_time_str or not duration_str:
        messages.error(request, "Veuillez renseigner l'heure de début et la durée.")
        return redirect("user_reservations")

    # Parse heure
    try:
        new_start_time = datetime.strptime(start_time_str, "%H:%M").time()
    except ValueError:
        messages.error(request, "Format d'heure invalide.")
        return redirect("user_reservations")

    # Parse durée
    try:
        new_duration = int(duration_str)
    except ValueError:
        messages.error(request, "Durée invalide.")
        return redirect("user_reservations")

    # Appliquer les nouvelles valeurs
    reservation.start_time = new_start_time
    reservation.duration_minutes = new_duration

    # Vérifier via clean() s'il y a overlap
    try:
        reservation.clean()
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect("user_reservations")

    reservation.save()
    messages.success(request, "Réservation mise à jour avec succès.")
    return redirect("user_reservations")


@login_required
@require_POST
def delete_reservation(request, reservation_id):
    """
    Supprime une réservation.
    """
    reservation = get_object_or_404(
        VenueReservation,
        pk=reservation_id,
        user=request.user,
    )
    reservation.delete()
    messages.success(request, "Réservation supprimée.")
    return redirect("user_reservations")
def generate_pdf(request, reservation_id):
    # Get the reservation object
    reservation = VenueReservation.objects.get(id=reservation_id)

    # Create a response object with the PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reservation_{reservation_id}.pdf"'

    # Create a PDF object
    p = canvas.Canvas(response)

    # Add content to the PDF
    p.drawString(100, 800, f"Venue: {reservation.venue.nom_v}")
    p.drawString(100, 780, f"Reservation Date: {reservation.date_reservation}")
    p.drawString(100, 760, f"Start Time: {reservation.start_time}")
    p.drawString(100, 740, f"Duration: {reservation.duration_minutes} minutes")

    # Save the PDF
    p.showPage()
    p.save()

    return response