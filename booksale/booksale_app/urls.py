from django.urls import path
from . import views
from booksale_app.views.admin_view.sanpham import (
    product_list,
    product_add,
    product_edit,
    product_delete,
    product_detail
)
from booksale_app.views.admin_view import category

try:
    from .views.employee import inventory_overview, inventory_import, inventory_export, supplier_list
    HAS_EMPLOYEE_VIEWS = True
except ImportError:
    HAS_EMPLOYEE_VIEWS = False

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # USER URL
    path('', views.home_view, name='home'),

    # EMPLOYEE URL
    path('emp/order_list/', views.order_list, name='emp/order_list'),
    path('emp/order_details/<int:pk>/', views.order_detail, name='emp/detail'),
    path('emp/order_confirm/<int:pk>/', views.order_detail, name='emp/confirm'),
    path('emp/order_cancel/<int:pk>/', views.order_detail, name='emp/cancel'),
    path('emp/order_confirm_status/<int:pk>/', views.order_confirm_status, name='emp/order_confirm_status'),
    path('emp/order_cancel_status/<int:pk>/', views.order_cancel_status, name='emp/order_cancel_status'),

    # CRUD sản phẩm
    path('emp/product/add/', product_add, name='product_add'),
    path('product/<int:pk>/edit/', product_edit, name='product_edit'),
    path('emp/product/<int:pk>/delete/', product_delete, name='product_delete'),
    path('emp/product', views.product_list, name='product_list'),
    path('emp/product-detail/<int:pk>/', product_detail, name='product_detail'),

    path("emp/category", category.category_list, name="category_list"),
    path("emp/category/add/", category.category_add, name="category_add"),
    path("emp/category/<int:pk>/delete/", category.category_delete, name="category_delete"),
    path('emp/category/<int:pk>/', category.category_detail, name='category_detail'),

    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('donhang/', views.donhang, name='donhang'),
    path('categories/', views.category_view, name='category'),
    path('categories/<int:pk>/', views.category_detail_view, name='category_detail'),
    path('product-detail-user/<int:pk>/', views.product_detail_user, name='product_detail_user'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]

# Thêm employee routes nếu có
if HAS_EMPLOYEE_VIEWS:
    urlpatterns += [
        path('employee/inventory_overview/', inventory_overview.inventory_list, name='inventory_list'),
        path('employee/inventory_import/', inventory_import.inventory_import, name='inventory_import'),
        path('employee/inventory_export/', inventory_export.inventory_export, name='inventory_export'),
        path('employee/supplier_list/', supplier_list.supplier_list, name='supplier_list'),
        path('employee/supplier_list/add/', supplier_list.supplier_add, name='supplier_add'),
        path('employee/supplier_list/edit/<int:pk>/', supplier_list.supplier_edit, name='supplier_edit'),
        path('employee/supplier_list/delete/<int:pk>/', supplier_list.supplier_delete, name='supplier_delete'),
    ]
