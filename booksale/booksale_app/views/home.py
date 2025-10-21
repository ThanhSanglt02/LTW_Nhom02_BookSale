from django.views import View
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home.html')

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html')