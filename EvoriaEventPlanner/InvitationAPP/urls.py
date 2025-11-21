from django.urls import path
from . import views

app_name = 'InvitationAPP'

urlpatterns = [
    path('', views.invitation_list, name='invitation_list'),
    path('<int:pk>/', views.invitation_detail, name='invitation_detail'),
    path('create/', views.invitation_create, name='invitation_create'),
    path('<int:pk>/update/', views.invitation_update, name='invitation_update'),
    path('<int:pk>/delete/', views.invitation_delete, name='invitation_delete'),

    path('<int:invitation_pk>/guests/', views.guest_list, name='guest_list'),
    path('<int:invitation_pk>/guests/create/', views.guest_create, name='guest_create'),
    path('<int:invitation_pk>/guests/<int:pk>/send/', views.guest_send_options, name='guest_send_options'),
    path('<int:invitation_pk>/guests/<int:pk>/update/', views.guest_update, name='guest_update'),
    path('<int:invitation_pk>/guests/<int:pk>/delete/', views.guest_delete, name='guest_delete'),
    path('event-info/<int:event_id>/', views.event_info, name='event_info'),
]
