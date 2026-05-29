from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail адрес")
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует!")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            clean_p = phone.replace(' ', '').replace('-', '')
            if not clean_p.replace('+', '').isdigit():
                raise forms.ValidationError("Номер телефона должен содержать только цифры, пробелы, дефисы и +!")
            if not (clean_p.startswith('+7') or clean_p.startswith('8')):
                raise forms.ValidationError("Номер должен начинаться с +7 или 8!")
        return phone