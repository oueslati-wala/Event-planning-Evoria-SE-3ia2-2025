from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profil_user, name='profil_user'),
    
]