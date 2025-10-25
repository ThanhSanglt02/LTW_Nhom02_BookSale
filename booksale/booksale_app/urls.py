from django.urls import path
from .views import home_view, product_detail, register_view, login_view

# from .views.home import HomeView
from . import views
urlpatterns = [
    path('',home_view, name='home'),
    path('product', views.product_list, name='product_list'),
    path('product-detail/', views.product_detail, name='product_detail'),
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name = 'register')
]

