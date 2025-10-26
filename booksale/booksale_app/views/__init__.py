# Import các hàm view từ home.py
from .home import index as home_view
from .sanpham import product_list
from .chitietsanpham import product_detail
from .authen_view import register_view, login_view, logout_view
from .admin_view.order_view import adm_order_list
# Import các hàm view từ product.py
# from .product import index as product_index, detail as product_detail