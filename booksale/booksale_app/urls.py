from django.urls import path
from .views import home_view, tonkho_list, product_detail

# from .views.home import HomeView
from . import views
urlpatterns = [
    path('',home_view, name='home'),
    path('stock/', tonkho_list, name = 'tonkho'),
    path('product', views.product_list, name='product_list'),
    path('product-detail/', views.product_detail, name='product_detail')
]

