from django.shortcuts import redirect, render
from .forms import UserProfileForm, UserRegisterForm
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login 
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .utils import account_activation_token
from .forms import LoginForm
from .forms import ForgotPasswordForm, ResetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator



import pyotp
import qrcode
import io
import base64

from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def profil(request):
    return render(request, "users/profil.html")

def profil_user(request):
    user = request.user

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profil")
    else:
        form = UserProfileForm(instance=user)

    return render(request, "users/profil_user.html", {"form": form})


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

            activation_link = (
                f"http://{current_site.domain}/users/activate/{uid}/{token}/"
            )

            subject = "Activate your account"
            html_message = render_to_string(
                "users/activation_email.html",
                {
                    "user": user,
                    "activation_link": activation_link,
                },
            )

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
            print(
                f"is_active={user.is_active}, last_login={user.last_login}, password_hash={user.password[:10]}..."
            )
    else:
        print("Utilisateur introuvable pour cet UID")

    return render(request, "users/activation_failed.html")

def login_view(request):
    error = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Récupération des champs validés
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            # Vérification manuelle de l'utilisateur
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user and user.check_password(password):
                # Création du secret 2FA si inexistant
                if not user.totp_secret:
                    user.totp_secret = pyotp.random_base32()
                    user.save()

                # Stockage temporaire pour la 2FA
                request.session["pre_2fa_user_id"] = user.pk
                return redirect("two_factor")
            else:
                error = "Identifiants invalides"
        else:
            # Formulaire invalide (captcha ou autres erreurs)
            error = "Veuillez vérifier le captcha et vos identifiants"
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "error": error})
# def login_view(request):
#     error = None
#     if request.method == "POST":
            

#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             user = None

#         if user is not None and user.check_password(password):
#             # Si le secret 2FA n'existe pas, on le crée
#             if not user.totp_secret:
#                 user.totp_secret = pyotp.random_base32()
#                 user.save()
#             request.session["pre_2fa_user_id"] = user.pk  # stocker temporairement
#             return redirect("two_factor")
#         else:
#             return render(request, "login.html", {"error": "Invalid credentials"})
#     return render(request, "login.html")

# def login_view(request):
#     error = None

#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")

#             # Vérifie l'utilisateur
#             user = authenticate(username=email, password=password)
#             if user:
#                 # Si le secret 2FA n'existe pas, on le crée
#                 if not user.totp_secret:
#                     user.totp_secret = pyotp.random_base32()
#                     user.save()
#                 request.session["pre_2fa_user_id"] = user.pk
#                 return redirect("two_factor")
#             else:
#                 error = "Identifiants invalides"
#         else:
#             # Le formulaire n'est pas valide (captcha ou autre)
#             error = "Veuillez vérifier le captcha et vos identifiants"
#     else:
#         form = LoginForm()

#     return render(request, "login.html", {"form": form, "error": error})


# page 2FA
def two_factor(request):
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(pk=user_id)

    # Générer QR code si l'utilisateur n'a pas scanné l'app
    totp_uri = pyotp.totp.TOTP(user.totp_secret).provisioning_uri(
        name=user.email, issuer_name="EvoriaApp"
    )
    # QR code en base64 pour affichage
    qr = qrcode.make(totp_uri)
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()

    if request.method == "POST":
        code = request.POST.get("code")
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(code):
            login(request, user)
            return redirect("profil")  # connecté avec succès
        else:
            return render(
                request,
                "users/two_factor.html",
                {"error": "Invalid 2FA code", "qr": qr_base64},
            )

    return render(request, "users/two_factor.html", {"qr": qr_base64})

def logout_view(req):
    logout(req)
    return redirect("login")
password_reset_token = PasswordResetTokenGenerator()

# Page pour demander la réinitialisation
def forgot_password(request):
    message_sent = False
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = password_reset_token.make_token(user)
                current_site = get_current_site(request)
                reset_link = f"http://{current_site.domain}/users/reset-password/{uid}/{token}/"

                subject = "Reset your password"
                html_message = render_to_string("users/password_reset_email.html", {
                    "user": user,
                    "reset_link": reset_link
                })

                email_msg = EmailMultiAlternatives(subject, "", to=[user.email])
                email_msg.attach_alternative(html_message, "text/html")
                email_msg.send()
            # # Toujours afficher le message pour ne pas révéler l’existence de l’email
            # return render(request, "users/check_reset_passwd_email.html",{"message_sent": True})
            message_sent =True
    else:
        form = ForgotPasswordForm()
        
    return render(request, "users/forgot_password.html", {
        "form": form,
        "message_sent": message_sent
        })

# Page pour entrer le nouveau mot de passe
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is None or not password_reset_token.check_token(user, token):
        return render(request, "users/activation_failed.html", {"message": "Lien de réinitialisation invalide ou expiré"})

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            user.set_password(new_password)
            user.save()
            return redirect("login")
    else:
        form = ResetPasswordForm()

    return render(request, "users/reset_password.html", {"form": form})
def index(request):
    session_expiry = request.session.get_expiry_age()
    return render(request, "index.html", {"session_expiry": session_expiry})