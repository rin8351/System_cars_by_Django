from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomParts(forms.ModelMultipleChoiceField):
    def label_from_instance(self, parts):
        return parts.model_p

class AddCars(forms.ModelForm):

    class Meta:
        model = cars
        fields = ['name', 'margin', 'parts']

    name=forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    margin=forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'min': '1', 'step': '1', 'class': 'form-input'}),
        help_text='Допуск должен быть больше 0'
    )
    parts=CustomParts(queryset=parts.objects.all(), widget=forms.CheckboxSelectMultiple)

    def create(self, commit=True):
        car = super().save(commit=False)
        car.save()
        for part in self.cleaned_data['parts']:
            car_part.objects.create(car=car, part=part, name=car.name)
        return car

    def save(self, *args, **kwargs):
        self.create()
        super().save(*args, **kwargs)
    
    def clean_margin(self):
        margin = self.cleaned_data.get('margin')
        if margin is not None and margin <= 0:
            raise forms.ValidationError('Допуск должен быть больше нуля.')
        return margin

class AddParts(forms.ModelForm):

    class Meta:
        model = parts
        fields = ['type', 'model_p','price', 'count_p', 'params']

    type=forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    model_p=forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    price=forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'min': '1', 'step': '1', 'class': 'form-input'}),
        help_text='Цена должна быть больше 0'
    )
    count_p=forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'min': '1', 'step': '1', 'class': 'form-input'}),
        help_text='Количество должно быть больше 0'
    )
    params=forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля.')
        return price
    
    def clean_count_p(self):
        count_p = self.cleaned_data.get('count_p')
        if count_p is not None and count_p <= 0:
            raise forms.ValidationError('Количество должно быть больше нуля.')
        return count_p


class registeruser(UserCreationForm):
    username= forms.CharField(label = 'Login',widget=forms.TextInput(attrs={'class':'form-input'}))
    email= forms.EmailField(label = 'Email',widget=forms.EmailInput(attrs={'class':'form-input'}))
    password1= forms.CharField(label = 'Password',widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2= forms.CharField(label = 'Password',widget=forms.PasswordInput(attrs={'class':'form-input'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    
class LoginUserForm(AuthenticationForm):
    username= forms.CharField(label = 'Login',widget=forms.TextInput(attrs={'class':'form-input'}))
    password= forms.CharField(label = 'Password',widget=forms.PasswordInput(attrs={'class':'form-input'}))
