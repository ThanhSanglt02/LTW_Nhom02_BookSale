from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
#   from .models import Product,ProductImageForm
from .models import Product, Genre

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True  # Tự động active tài khoản
        if commit:
            user.save()
        return user


class ProductForm(forms.ModelForm):
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full border border-gray-300 rounded-lg p-3 text-gray-800 focus:ring-2 focus:ring-green-400 focus:outline-none'
        })
    )

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['cart', 'order']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-3 text-gray-800 focus:ring-2 focus:ring-green-400 focus:outline-none'
            }),
            'publisher': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-3 text-gray-800 focus:ring-2 focus:ring-green-400 focus:outline-none'
            }),
        }
