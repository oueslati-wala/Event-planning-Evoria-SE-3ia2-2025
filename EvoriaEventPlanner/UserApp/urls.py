from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('profile/', login_required(views.profil), name='profil'),
    path('edit/', login_required(views.profil_user), name='profil_user'),
    # path('login',LoginView.as_view(template_name="login.html"),name="login"),
    path('login/', (views.login_view), name='login'),
    path( "register/", views.register , name="register"),
    path('logout/',views.logout_view, name="logout"),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('two-factor/', views.two_factor, name='two_factor'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", views.reset_password, name="reset_password"),
    
]