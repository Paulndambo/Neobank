from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from apps.users.models import UserOTP, User
# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import random

User = get_user_model()  # Get the user model

def login_user(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']  # Can be username or email
        password = request.POST['password']

        # Check if identifier is an email
        if "@" in identifier:
            try:
                user = User.objects.get(email=identifier)
                username = user.username  # Get corresponding username
            except User.DoesNotExist:
                return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
        else:
            username = identifier  # It's a username

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['otp_verified'] = False  
            request.session['otp'] = str(random.randint(100000, 999999))  
            request.session['next_url'] = request.GET.get('next', 'home')

            # Here, send OTP to the user (email/SMS)
            print(f"OTP for {user.username}: {request.session['otp']}")  # Debugging

            return redirect('verify-otp')  # Redirect to OTP page
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    next_url = request.GET.get('next', '')
    return render(request, 'accounts/login.html', {'next': next_url})




def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            password=password,
            phone=phone_number
        )
        user.set_password(password)
        user.save()

        return redirect("login")

    return render(request, "accounts/register.html")


@login_required
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        print(f"Otp: {entered_otp}, Stored OTP: {stored_otp}")

        if entered_otp == stored_otp:
            request.session['otp_verified'] = True
            #next_url = request.session.pop('next_url', 'index')  # Get and remove next_url
            return redirect("otp-success")  # Redirect to the protected page
        else:
            return render(request, 'accounts/otp.html', {'error': 'Invalid OTP'})

    return render(request, 'accounts/otp.html')


def otp_success(request):
    return render(request, "accounts/otp_success.html")


@login_required
def logout_user(request):
    user = request.user
    user.otp_verified = False
    user.save()
    logout(request)
    return redirect("/")