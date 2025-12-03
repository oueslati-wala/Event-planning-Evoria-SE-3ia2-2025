from django.shortcuts import redirect, render
from .forms import UserProfileForm, UserRegisterForm
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from .utils import account_activation_token
# Create your views here.
def profil(request):
    return render(request, 'users/profil.html')
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
# # Create your views here.
# def register(request):
#     if request.method == "POST":
#          # Process registration data here
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # You might want to redirect to a success page or login page after registration
#             return redirect("login")  # Assuming you have a URL pattern named 'login'
#     else:
#         form = UserRegisterForm()
#         return render(request, 'register.html', {'form': form})
#     return render(request, "register.html", {"form":form})
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # IMPORTANT
            user.save()

            # Préparation du mail
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            activation_link = f"http://{current_site.domain}/users/activate/{uid}/{token}/"

            subject = "Activate your account"
            html_message = render_to_string("users/activation_email.html", {
                "user": user,
                "activation_link": activation_link,
            })

            email = EmailMultiAlternatives(subject, "", to=[user.email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            return render(request, "users/check_email.html")

    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


# def activate_account(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         user = None
#     # if user:
#     # # Affiche le statut actuel de is_active dans la console
#     #     print(f"Utilisateur: {user.username}, is_active = {user.is_active}")
#     if user and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect("profil")
#     #Affiche le statut actuel de is_active dans la console
#     # print(f"Utilisateur actuel is_active = {user.is_active}")
#     return render(request, "users/activation_failed.html")
def activate_account(request, uidb64, token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(f"Utilisateur trouvé: {user.username}, is_active={user.is_active}")
    except Exception as e:
        print("Erreur récupération utilisateur:", e)
        user = None

    if user is not None:
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            print(f"Activation réussie pour {user.username}")
            return redirect("profil")
        else:
            print(f"Token invalide pour {user.username}")
            print(f"is_active={user.is_active}, last_login={user.last_login}, password_hash={user.password[:10]}...")
    else:
        print("Utilisateur introuvable pour cet UID")

    return render(request, "users/activation_failed.html")
    

def logout_view(req):
    logout(req)
    return redirect("login")