
from django.urls import path
from .views import decor_detail, edit_reservation, generate_pdf, index, user_reservations, venues_list, reserve_venue,delete_reservation  # ← ajoute reserve_venue
from . import views  # Add this import

urlpatterns = [
    path('', index, name='index'),
    path('venues/', venues_list, name='venues_list'),
    path('venues/<int:venue_id>/reserve/', reserve_venue, name='reserve_venue'),  # ← nouvelle route
    path('decor/<int:decor_id>/', decor_detail, name='decor_detail'),
    path('my-reservations/', user_reservations, name='user_reservations'),
    path('reservations/<int:reservation_id>/edit/', edit_reservation, name='edit_reservation'),
    path('reservations/<int:reservation_id>/delete/', delete_reservation, name='delete_reservation'),
    path('reservation/<int:reservation_id>/pdf/', generate_pdf, name='generate_reservation_pdf'),

]
