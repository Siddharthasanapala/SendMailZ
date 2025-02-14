from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'sender_email', 'key')

class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'sender_email', 'key')

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6)