from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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

