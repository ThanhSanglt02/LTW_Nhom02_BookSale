from django.urls import path
from . import views
from booksale_app.views.admin_view.sanpham import (
    product_add,
    product_edit,
    product_delete,
    product_detail,
    product_bulk_delete
)
from booksale_app.views.admin_view import category, genre
from .views.employee import inventory_overview, inventory_import, inventory_export, supplier_list

# try:
#     from .views.employee import inventory_overview, inventory_import, inventory_export, supplier_list
#     HAS_EMPLOYEE_VIEWS = True
# except ImportError:
#     HAS_EMPLOYEE_VIEWS = False

urlpatterns = [

    # USER URLS
    path('', views.home_view, name='home'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete/', views.delete_cart_items, name='delete_cart_items'),
    path('cart/proceed-to-order/', views.proceed_to_order, name='proceed_to_order'),
    path('order/', views.order, name='order'),
    path('order/create/', views.create_order, name='create_order'),
    path('order_confirm/<int:order_id>/', views.order_confirm, name='order_confirm'),
    path('order_confirm/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('categories/', views.category_view, name='category'),
    path('categories/<str:category_name>/', views.category_detail_view, name='category_detail'),
    path('product-detail-user/<int:pk>/', views.product_detail_user, name='product_detail_user'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
    path('search/', views.search_view, name='search'),
    path('product-detail-user/<int:product_id>/review/', views.submit_review, name='submit_review'),
    path('profile/', views.profile, name='profile'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('buy-again/<int:order_id>/', views.buy_again, name='buy_again'),
    path('order/<int:order_id>/review/', views.review_order, name='review_order'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),


    # EMPLOYEE SALE URLS
    # path('emp/order_list/', views.order_list, name = 'emp/order_list'),
    path('emp/order_list/', views.order_list, name = 'emp/order_list'),
    path('emp/order_list_waiting/', views.order_list_waiting, name = 'emp/order_list_waiting'),
    path('emp/order_details/<int:pk>/', views.order_detail, name = 'order_detail'),
    path('emp/order_confirm/<int:pk>/', views.order_detail, name = 'emp/confirm'),
    path('emp/order_cancel/<int:pk>/', views.order_detail, name = 'emp/cancel'),
    path('emp/order_completed/<int:pk>/', views.order_detail, name = 'emp/completed'),
    path('emp/order_confirm_status/<int:pk>/', views.order_confirm_status, name='emp/order_confirm_status'),
    path('emp/order_cancel_status/<int:pk>/', views.order_cancel_status, name='emp/order_cancel_status'),  
    # CRUD sản phẩm
    path('emp/product/add/', product_add, name='product_add'),
    path('emp/product/<int:pk>/edit/', product_edit, name='product_edit'),
    path('emp/product/<int:pk>/delete/', product_delete, name='product_delete'),
    path('emp/product', views.product_list, name='product_list'),
    path('emp/product-detail/<int:pk>/', product_detail, name='product_detail'),
    path('emp/product/delete/bulk/', product_bulk_delete, name='product_bulk_delete'),

    path("emp/category", category.category_list, name="category_list"),
    path("emp/category/add/", category.category_add, name="category_add"),
    path("emp/category/<int:pk>/delete/", category.category_delete, name="category_delete"),
    path('emp/category/<int:pk>/', category.category_detail, name='category_detail'),
    path('emp/category/delete/bulk/', category.category_bulk_delete, name='category_bulk_delete'),

    path('emp/genre/', genre.genre_list, name='genre_list'),
    path('emp/genre/add/', genre.genre_add, name='genre_add'),
    path('emp/genre/detail/<int:pk>', genre.genre_detail, name='genre_detail'),
    path('emp/genre/<int:pk>/edit', genre.genre_edit, name='genre_edit'),
    path('emp/genre/<int:pk>/delete', genre.genre_delete, name='genre_delete'),
    path('emp/genre/delete/bulk/', genre.genre_bulk_delete, name='genre_bulk_delete'),

    

    # EMPLOYEE STOCK URLS
    #    path('product-detail/', views.product_detail, name='product_detail'),
    #    path('product/', views.product_list, name='product_list'),
    path('employee/inventory_overview/', inventory_overview.inventory_list, name='inventory_list'),
    path('employee/inventory_import/', inventory_import.inventory_import, name='inventory_import'),
    path('employee/inventory_export/', inventory_export.inventory_export, name='inventory_export'),
    path('employee/supplier_list/', supplier_list.supplier_list, name='supplier_list'),
    path('employee/supplier_list/add/', supplier_list.supplier_add, name='supplier_add'),
    path('employee/supplier_list/edit/<int:pk>/', supplier_list.supplier_edit, name='supplier_edit'),
    path('employee/supplier_list/delete/<int:pk>/', supplier_list.supplier_delete, name='supplier_delete'),

    
    # path('product-detail/', views.product_detail, name='product_detail'),

    # path('product/', views.product_list, name='product_list'),

]

# Thêm employee routes nếu có
# if HAS_EMPLOYEE_VIEWS:
#     urlpatterns += [
#         path('employee/inventory_overview/', inventory_overview.inventory_list, name='inventory_list'),
#         path('employee/inventory_import/', inventory_import.inventory_import, name='inventory_import'),
#         path('employee/inventory_export/', inventory_export.inventory_export, name='inventory_export'),
#         path('employee/supplier_list/', supplier_list.supplier_list, name='supplier_list'),
#         path('employee/supplier_list/add/', supplier_list.supplier_add, name='supplier_add'),
#         path('employee/supplier_list/edit/<int:pk>/', supplier_list.supplier_edit, name='supplier_edit'),
#         path('employee/supplier_list/delete/<int:pk>/', supplier_list.supplier_delete, name='supplier_delete'),
#     ]
