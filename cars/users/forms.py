from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label = 'Login',
                widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label = 'Password',
                widget=forms.PasswordInput(attrs={'class':'form-input'}))
    

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled = True, label = 'Login',
                widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.EmailField(disabled = True, label = 'Email',
                widget=forms.EmailInput(attrs={'class':'form-input'}))
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-input'}),
            'last_name': forms.TextInput(attrs={'class':'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label = 'Old password',
                widget=forms.PasswordInput(attrs={'class':'form-input'}))
    new_password1 = forms.CharField(label = 'New password',
                widget=forms.PasswordInput(attrs={'class':'form-input'}))
    new_password2 = forms.CharField(label = 'New password confirmation',
                widget=forms.PasswordInput(attrs={'class':'form-input'}))
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']