from django.urls import path
from .views import (
    liste_animations,
    AnimateurList, AnimateurDetail, AnimateurCreate, AnimateurUpdate, AnimateurDelete,
    ResList, ResCreate, ResDetail, ResUpdate, ResDelete,
)

app_name = "animationapp"

urlpatterns = [
    path("", liste_animations, name="home"),
    path("animateurs/", AnimateurList.as_view(), name="anim_list"),
    path("animateurs/new/", AnimateurCreate.as_view(), name="anim_create"),
    path("animateurs/<int:pk>/", AnimateurDetail.as_view(), name="anim_detail"),
    path("animateurs/<int:pk>/edit/", AnimateurUpdate.as_view(), name="anim_update"),
    path("animateurs/<int:pk>/del/", AnimateurDelete.as_view(), name="anim_delete"),

    path("reservations/", ResList.as_view(), name="res_list"),
    path("reservations/new/", ResCreate.as_view(), name="res_create"),
    path("reservations/<int:pk>/", ResDetail.as_view(), name="res_detail"),
    path("reservations/<int:pk>/edit/", ResUpdate.as_view(), name="res_update"),
    path("reservations/<int:pk>/del/", ResDelete.as_view(), name="res_delete"),
]
