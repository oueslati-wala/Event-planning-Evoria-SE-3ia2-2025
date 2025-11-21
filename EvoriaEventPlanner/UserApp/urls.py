from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('profile/', views.profil, name='profil'),
    path('edit/', views.profil_user, name='profil_user'),
    path('login',LoginView.as_view(template_name="login.html"),name="login"),
    path( "register/", views.register , name="register"),
    path('logout/',views.logout_view, name="logout")
]