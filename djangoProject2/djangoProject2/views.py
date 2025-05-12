from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from guides.models import Guides
from products.models import CPU, MOBO, CPUCooler, RAM, Storage, GPU, PSU, CASE


def base(request):
    return render(request,'base.html')


def home(request):
    guides = Guides.objects.all()
    return render(request, 'components/home.html', {'guides': guides})

def builder(request):
    return render(request, 'components/builder.html')


def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        bio = request.POST.get('bio')

        if not uname or not email or not pw1 or not pw2:
            messages.error(request, "All fields are required.")
            return render(request, 'registration/register.html')

        if pw1 != pw2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration/register.html')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'registration/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'registration/register.html')

        try:
            my_user = User.objects.create_user(
                username=uname,
                email=email,
                password=pw1,
                first_name=first_name,
                last_name=last_name
            )
            my_user.save()


            user_profile, created = UserProfile.objects.get_or_create(
                user=my_user,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone_number": phone_number,
                    "address": address,
                    "date_of_birth": date_of_birth,
                    "bio": bio
                }
            )

            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred while creating the account: {e}")
            return render(request, 'registration/register.html')

    return render(request, 'registration/register.html')

def LOGIN(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return HttpResponse("Username or password is incorrect!")

    return render(request, 'registration/login.html')

def LOGIN(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or password is incorrect!")

    return render(request, 'registration/login.html')


def LOGOUT(request):
    logout(request)
    return redirect("home")