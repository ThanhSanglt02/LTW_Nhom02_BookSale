from django.urls import path
from .views import home_view, product_detail, register_view, login_view, logout_view, order_list

# from .views.home import HomeView
from . import views
from django.urls import path
from .views import home_view, product_detail, register_view, login_view, logout_view, order_detail
from django.shortcuts import render, redirect, get_object_or_404
from booksale_app.views.admin_view.sanpham import (
    product_list,
    product_add,
    product_edit,
    product_delete,
    product_detail
)
from booksale_app.views.admin_view import category
from booksale_app.models import Category
from . import views
urlpatterns = [
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('register/', views.register_view, name = 'register'),


    # USER URL
    path('',home_view, name='home'),
    

    # EMPLOYEE URL
    path('emp/order_list/', views.order_list, name = 'emp/order_list'),
    path('emp/order_details/<int:pk>/', views.order_detail, name = 'emp/detail'),
    path('emp/order_confirm/<int:pk>/', views.order_detail, name = 'emp/confirm'),
    path('emp/order_cancel/<int:pk>/', views.order_detail, name = 'emp/cancel'),
    path('emp/order_confirm_status/<int:pk>/', views.order_confirm_status, name='emp/order_confirm_status'),
    path('emp/order_cancel_status/<int:pk>/', views.order_cancel_status, name='emp/order_cancel_status'),   
#    path('product-detail/', views.product_detail, name='product_detail'),
#    path('product/', views.product_list, name='product_list'),

    # CRUD sản phẩm
    path('emp/product/add/', product_add, name='product_add'),
    path('product/<int:pk>/edit/', product_edit, name='product_edit'),
    path('emp/product/<int:pk>/delete/', product_delete, name='product_delete'),
    path('emp/product', views.product_list, name='product_list'),
    path('emp/product-detail/<int:pk>/', product_detail, name='product_detail'),

    path("emp/category", category.category_list, name="category_list"),
    path("emp/category/add/", category.category_add, name="category_add"),
    # path("category/edit/<int:pk>/", category.category_edit, name="category_edit"),
    path("emp/category/<int:pk>/delete/", category.category_delete, name="category_delete"),
    path('emp/category/<int:pk>/', category.category_detail, name='category_detail'),
    # path('adm/order/<int:pk>/', views.edit_order, name = 'adm/edit_order'),
    # path('adm/order/new/', views.edit_order, name = 'adm/edit_order'),

]

