from django.urls import path
from .views import decor_detail, index, user_reservations, friends_reservations, venues_list, reserve_venue

urlpatterns = [
    path('', index, name='index'),
    path('venues/', venues_list, name='venues_list'),
    path('venues/<int:venue_id>/reserve/', reserve_venue, name='reserve_venue'),  # ← nouvelle route
    path('decor/<int:decor_id>/', decor_detail, name='decor_detail'),
    path('my-reservations/', user_reservations, name='user_reservations'),
    path('friends-reservations/', friends_reservations, name='friends_reservations'),
]
