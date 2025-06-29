from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.contrib import messages
import random


def register_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            request.session['email'] = email
            return redirect('login_password')  # asosiy sahifaga yo'naltirish
        else:
            request.session['email'] = email
            return redirect('register_name')
    return render(request=request, template_name='account/email.html')

def login_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        email = request.session.get('email')

        if not email:
            # Email sessiyada yo'q bo‘lsa, login sahifasiga qaytarish
            messages.error(request, "Sessiya muddati tugagan. Iltimos, emailingizni qaytadan kiriting.")
            return redirect('register_email')  # Emailni kiritish sahifasi nomi

        user = authenticate(request, email=email, password=password1)
        if user is not None:
            login(request, user)
            return redirect('home')  # Asosiy sahifaga yo'naltirish
        else:
            messages.error(request, "Parol noto‘g‘ri. Iltimos, qayta urinib ko‘ring.")
            return render(request, 'account/login_password.html')

    return render(request, 'account/login_password.html')

def register_name(request):
    if request.method == 'POST':
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        return redirect('register_password')
    return render(request, 'account/name.html')


def register_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        if len(password1) < 8:
            messages.error(request, "Parol kamida 8 ta belgidan iborat bo‘lishi kerak ❗️")
            return render(request, 'account/password.html')

        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Parollar mos kelmadi')
            return redirect('register_password')
        request.session['password'] = password1
        return redirect('register_verify')
    return render(request, 'account/password.html')


def register_verify(request):
    if request.method == 'POST':
        code_entered = request.POST.get('code')
        if code_entered == request.session.get('verification_code'):
            return redirect('register_complete')
        else:
            messages.error(request, 'Kod noto‘g‘ri')
            return redirect('register_verify')

    # Kod yuboriladi
    code = str(random.randint(100000, 999999))
    request.session['verification_code'] = code
    email = request.session.get('email')
    send_mail(
        'Tasdiqlash kodi',
        f'Sizning tasdiqlash kodingiz: {code}',
        'noreply@yourdomain.com',
        [email],
        fail_silently=False,
    )
    return render(request, 'account/verify.html')


def register_complete(request):
    email = request.session.get('email')
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    password = request.session.get('password')

    if not CustomUser.objects.filter(email=email).exists():
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)

    # Sessionni tozalash
    for key in ['email', 'first_name', 'last_name', 'password', 'verification_code']:
        request.session.pop(key, None)

    return render(request, 'account/complete.html')

def log_out(request):
    print(request.user.is_authenticated)  # Foydalanuvchini autentifikatsiyasini tekshirish
    if request.user.is_authenticated:
        logout(request)  # Foydalanuvchini chiqish qilamiz
        return redirect('register_email')  # Login sahifasiga yo'naltiramiz
    return redirect('register_email')