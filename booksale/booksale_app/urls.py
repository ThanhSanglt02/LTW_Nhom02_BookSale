from django.urls import path
from .views import home_view, tonkho_list
# from .views.home import HomeView

urlpatterns = [
    path('',home_view, name='home'),
    path('stock/', tonkho_list, name = 'tonkho')
]