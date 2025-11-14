# AnimationApp/urls.py
from django.urls import path
from .views import (
    AnimateurList, AnimateurDetail,
    ResList, ResCreate, ResDetail, ResUpdate, ResDelete,
)

app_name = "animationapp"

urlpatterns = [
    path("animateurs/",               AnimateurList.as_view(),  name="anim_list"),
    path("animateurs/<int:pk>/",      AnimateurDetail.as_view(),name="anim_detail"),

    path("reservations/",               ResList.as_view(),  name="res_list"),
    path("reservations/new/",           ResCreate.as_view(),name="res_create"),
    path("reservations/<int:pk>/",      ResDetail.as_view(),name="res_detail"),
    path("reservations/<int:pk>/edit/", ResUpdate.as_view(),name="res_update"),
    path("reservations/<int:pk>/del/",  ResDelete.as_view(),name="res_delete"),
]
