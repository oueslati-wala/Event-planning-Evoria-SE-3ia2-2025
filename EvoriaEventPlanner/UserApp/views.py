from django.shortcuts import redirect, render
from .forms import UserProfileForm, UserRegisterForm
from django.contrib.auth import logout
# Create your views here.
def profil(request):
    user = request.user
    return render(request, 'users/profil.html', {'user': user})
def profil_user(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'users/profil_user.html', {'form': form})
# Create your views here.
def register(request):
    if request.method == "POST":
         # Process registration data here
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # You might want to redirect to a success page or login page after registration
            return redirect("login")  # Assuming you have a URL pattern named 'login'
    else:
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})
    return render(request, "register.html", {"form":form})
def logout_view(req):
    logout(req)
    return redirect("login")