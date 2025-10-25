from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..forms import CreateUserForm

def register_view(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        print("cos loi xay ra")
    context = {'form': form}
    return render(request, 'register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        # if request.user.is_superuser:
        #     return redirect('admin')  # URL name cho admin
        # else:
        return redirect('home')   # URL name cho user
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password') 
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
            #  # Kiểm tra phân quyền
            # if user.is_superuser:
            #     return redirect('admin')
            # else:
            print("cos loi 1")
            return redirect('home')
            
        else: messages.info(request, 'user or password is not correct!')
    print("co loi 2")
    return render(request, 'login_temp.html')

# def logout_view(request):
#     logout(request)
    # return redirect('login')
