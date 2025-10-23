from django.urls import path
from .views import home_view, tonkho_list, product_detail

# from .views.home import HomeView

urlpatterns = [
    path('',home_view, name='home'),
    path('stock/', tonkho_list, name = 'tonkho'),
    path('product_detail/', product_detail, name='product_detail')
]