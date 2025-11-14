from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Animateur, ReservationAnim
from .forms import AnimateurForm, ReservationForm

from django.shortcuts import render

def accueil(request):
    return render(request, 'index.html')

from django.http import HttpResponse
def home(request):
    return HttpResponse("Bienvenue sur projet_se ✨")
# views.py
def liste_animations(request):
    items = Animateur.objects.all()
    return render(request, 'animation.html', {'animations': items})



# ---- Animateur ----
class AnimateurList(ListView):
    model = Animateur
    template_name = "AnimationApp/animateur_list.html"
    context_object_name = "animations"

class AnimateurDetail(DetailView):
    model = Animateur
    template_name = "AnimationApp/animateur_detail.html"

class AnimateurCreate(CreateView):
    model = Animateur
    form_class = AnimateurForm
    template_name = "AnimationApp/animateur_form.html"
    success_url = reverse_lazy("animationapp:anim_list")
    def form_valid(self, form):
        messages.success(self.request, "Animateur créé avec succès.")
        return super().form_valid(form)

class AnimateurUpdate(UpdateView):
    model = Animateur
    form_class = AnimateurForm
    template_name = "AnimationApp/animateur_form.html"
    success_url = reverse_lazy("animationapp:anim_list")
    def form_valid(self, form):
        messages.success(self.request, "Animateur mis à jour.")
        return super().form_valid(form)

class AnimateurDelete(DeleteView):
    model = Animateur
    template_name = "AnimationApp/animateur_confirm_delete.html"
    success_url = reverse_lazy("animationapp:anim_list")
    def delete(self, request, *a, **kw):
        messages.success(self.request, "Animateur supprimé.")
        return super().delete(request, *a, **kw)

# ---- Réservation ----
class ResList(ListView):
    model = ReservationAnim
    template_name = "AnimationApp/reservationanim_list.html"
    context_object_name = "items"
    paginate_by = 10
    ordering = ["-date_debut"]

class ResDetail(DetailView):
    model = ReservationAnim
    template_name = "AnimationApp/reservationanim_detail.html"

class ResCreate(CreateView):
    model = ReservationAnim
    form_class = ReservationForm
    template_name = "AnimationApp/reservationanim_form.html"
    success_url = reverse_lazy("animationapp:res_list")
    def get_initial(self):
        initial = super().get_initial()
        animateur_id = self.request.GET.get("animateur")
        if animateur_id:
            initial["animateur"] = animateur_id
        return initial
    def form_valid(self, form):
        messages.success(self.request, "Réservation enregistrée.")
        return super().form_valid(form)

class ResUpdate(UpdateView):
    model = ReservationAnim
    form_class = ReservationForm
    template_name = "AnimationApp/reservationanim_form.html"
    success_url = reverse_lazy("animationapp:res_list")
    def form_valid(self, form):
        messages.success(self.request, "Réservation mise à jour.")
        return super().form_valid(form)

class ResDelete(DeleteView):
    model = ReservationAnim
    template_name = "AnimationApp/reservationanim_confirm_delete.html"
    success_url = reverse_lazy("animationapp:res_list")
    def delete(self, request, *a, **kw):
        messages.success(self.request, "Réservation supprimée.")
        return super().delete(request, *a, **kw)
