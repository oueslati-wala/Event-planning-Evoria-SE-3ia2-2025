from django.shortcuts import redirect, render
from .forms import UserProfileForm
# Create your views here.
def profil_user(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'users/profil_user.html', {'form': form})