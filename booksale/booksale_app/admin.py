from django.contrib import admin
from booksale_app.models import (Customer, Order, Product, Category, Publisher, Order_Item, Cart, Cart_Item) 

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_name', 'email','phone')
    list_filter = ('cust_name',)
    search_fields = ('cust_name',)
   

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'order_date', 'status')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'unit_price')

# Muốn có model nào trên giao diện admin thì phải đăng ký model đó, nếu có chỉnh sửa thao tác thì phải thêm tham số class
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin) 
admin.site.register(Product)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Order_Item)
admin.site.register(Cart)
admin.site.register(Cart_Item, CartItemAdmin)



