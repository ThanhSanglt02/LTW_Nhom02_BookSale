from django.urls import path
from .views import home_view, product_detail, register_view, login_view, logout_view, order_list

# from .views.home import HomeView
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
    path('product-detail/', views.product_detail, name='product_detail'),
    path('product/', views.product_list, name='product_list'),
    
    
    # path('adm/order/<int:pk>/', views.edit_order, name = 'adm/edit_order'),
    # path('adm/order/new/', views.edit_order, name = 'adm/edit_order'),

]

