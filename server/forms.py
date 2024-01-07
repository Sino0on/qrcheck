from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm

from server.models import Para, Grade

User = get_user_model()


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'exampleInputPassword1'})
        }


class ParaForm(forms.ModelForm):
    class Meta:
        fields = ['lesson']
        model = Para


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-control'
                                          }),
    )
    password2 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-control'
                                          }),
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        fields = ['grade']
        model = Grade
