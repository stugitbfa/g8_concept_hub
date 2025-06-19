from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings

from functools import wraps

from .models import user
from .helpers import *

import random

# Create your views here.


def sign_in_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('sign_in')  # redirect to sign_in page
        return view_func(request, *args, **kwargs)
    return wrapper


def sign_in(request):
    if request.method == 'POST':
        email_ = request.POST['email'] 
        password_ = request.POST['password'] 

        if not user.objects.filter(email=email_).exists():
            print("Email does't exist")
            return redirect('sign_in')
        
        get_user = user.objects.get(email=email_)

        if not get_user.is_active:
            print("Your account is deactive please contact to customer care")
            return redirect('sign_in')
        is_password_verify = check_password(password_, get_user.password)
        if not is_password_verify:
            print("Email or password not match")
            return redirect('sign_in') 
        
        request.session['user_id'] = str(get_user.cid)
        return redirect('index')


    return render(request, 'dashboard/sign_in.html')

def sign_up(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']

        if not is_email_verified:
            print("Invalid email")
            return redirect('sign_up')

        if user.objects.filter(email=email_).exists():
            print("Email already exist")
            return redirect('sign_up')
        
        if not is_valid_mobile_number(mobile_):
            print("Invalid mobile")
            return redirect('sign_up')
        
        if user.objects.filter(mobile=mobile_).exists():
            print("Mobile already exist")
            return redirect('sign_up')
        
        if password_ != confirm_password_:
            print("Password and confirm password does't match") 
            return redirect('sign_up')
        
        if not is_valid_password(password_)[0]:
            print(is_valid_password(password_)[1])
            return redirect('sign_up')
        
        print(make_password(password_), '------')
        new_user = user.objects.create(
            email=email_,
            mobile=mobile_,
            password=make_password(password_)
        )
        new_user.save()

        otp = random.randint(111111,999999)

        subject = "Email Conformation mail | Workbook"
        message = f"""
        Hello user,

        Thank you for registering with Workbook.

        Your One-Time Password (OTP) for email verification is: {otp}

        Please enter this OTP to complete your registration. 

        If you did not initiate this request, please ignore this email.

        Best regards,  
        Workbook Team
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [f"{email_}"]
        send_mail(subject, message, from_email, recipient_list)
        new_user.otp = otp
        new_user.save()
        print("Please check your mail for email confirmation. Your registraion has been successfully done.")
        context = {
            'email': email_
        }
        return render(request, 'dashboard/email_verify.html', context)
        
    return render(request, 'dashboard/sign_up.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        # Send a simple reset link
        subject = 'Reset Your Password'
        message = 'Click here to reset your password: http://127.0.0.1:8000/reset-password/'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return render(request, 'dashboard/forgot_password.html', {
            'message': 'We sent a reset link to your email!'
        })

    return render(request, 'dashboard/forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # optional, see note below
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user_obj = user.objects.get(email=email)
                user_obj.password = make_password(new_password)
                user_obj.save()
                messages.success(request, "Password reset successful.")
                return redirect('sign_in')
            except user.DoesNotExist:
                messages.error(request, "No user found with this email.")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'dashboard/reset_password.html')
    

def email_verify(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        otp_ = request.POST['otp']

        get_user = user.objects.get(email=email_)

        if otp_ != get_user.otp:
            print("Invalid OTP")
            context = {
            'email': email_
            }
            return render(request, 'dashboard/email_verify.html', context)

        get_user.is_active = True
        get_user.save()
        return redirect('sign_in')

    return render(request, 'dashboard/email_verify.html')

@sign_in_required
def index(request):
    return render(request, 'dashboard/index.html')

@sign_in_required
def profile(request):
    return render(request, 'dashboard/profile.html')

@sign_in_required
def logout(request):
    del request.session['user_id']
    print("Now, you are logged Out")
    return redirect('sign_in')
    