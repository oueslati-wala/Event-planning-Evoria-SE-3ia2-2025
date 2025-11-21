from django.urls import path
from . import views

app_name = 'CateringAPP'

urlpatterns = [
    path('', views.front_portal, name='front_portal'),
    path('reserve/<int:caterer_id>/', views.reserve_catering, name='reserve_catering'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('choose/', views.caterer_choose_list, name='caterer_choose_list'),
    path('choose/<int:pk>/', views.caterer_choose, name='caterer_choose'),
    path('caterers/', views.caterer_list, name='caterer_list'),
    path('caterers/create/', views.caterer_create, name='caterer_create'),
    path('caterers/<int:pk>/update/', views.caterer_update, name='caterer_update'),
    path('caterers/<int:pk>/delete/', views.caterer_delete, name='caterer_delete'),

    path('menu/', views.menu_list, name='menu_list'),
    path('menu/create/', views.menu_create, name='menu_create'),
    path('menu/<int:pk>/update/', views.menu_update, name='menu_update'),
    path('menu/<int:pk>/delete/', views.menu_delete, name='menu_delete'),
]
