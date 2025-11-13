from django.views import View
from django.shortcuts import render

# Create your views here.

def home_view(request):
    return render(request, 'user_temp/home.html')

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html')