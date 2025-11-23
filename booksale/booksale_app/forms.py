from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Product, Genre, Supplier, Order, Order_Item

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



class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['sup_name', 'email', 'phone', 'address']
        labels = {
            'sup_name': 'Tên nhà cung cấp',
            'email': 'Email',
            'phone': 'Số điện thoại',
            'address': 'Địa chỉ',
        }
        widgets = {
            'sup_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none',
                'placeholder': 'VD: Nhà sách Minh Long'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none',
                'placeholder': 'example@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none',
                'placeholder': 'Nhập số điện thoại'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none',
                'rows': 3,
                'placeholder': 'VD: 123 Nguyễn Trãi, Hà Nội'
            }),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'shipping_date', 'note']
