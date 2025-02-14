import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, SignInForm, UpdateProfileForm, ForgotPasswordForm, OTPVerificationForm

class WelcomeView(View):
    def get(self, request):
        return render(request, 'welcome.html')

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'signup.html', {'form': form})

class SignInView(View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'signin.html', {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'signin.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('signin')

def profile(request):
    return render(request, 'profile.html')

def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'forgot_password.html', {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            User = get_user_model()
            try:
                user = User.objects.get(username=username, email=email)
                otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                request.session['reset_otp'] = otp
                request.session['reset_user_id'] = user.id
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    'siddharthasanapala136@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return redirect('verify_otp')
            except User.DoesNotExist:
                form.add_error(None, "No user found with the provided username and email.")
        return render(request, 'forgot_password.html', {'form': form})

class VerifyOTPView(View):
    def get(self, request):
        form = OTPVerificationForm()
        return render(request, 'verify_otp.html', {'form': form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            stored_otp = request.session.get('reset_otp')
            if entered_otp == stored_otp:
                user_id = request.session.get('reset_user_id')
                User = get_user_model()
                user = User.objects.get(id=user_id)
                login(request, user)
                del request.session['reset_otp']
                del request.session['reset_user_id']
                return redirect('home')
            else:
                form.add_error(None, "Invalid OTP. Please try again.")
        return render(request, 'verify_otp.html', {'form': form})