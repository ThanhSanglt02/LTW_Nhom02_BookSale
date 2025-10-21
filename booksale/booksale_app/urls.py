from django.urls import path
from .views import home_view
# from .views.home import HomeView

urlpatterns = [
    path('',home_view, name='home')

]