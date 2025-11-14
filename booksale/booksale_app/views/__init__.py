# Import các hàm view từ home.py
from .user_view.home import home_view
# Import các hàm view từ product.py
# from .product import index as product_index, detail as product_detail
from .admin_view.sanpham import product_list
from .admin_view.chitietsanpham import product_detail
from .authen_view import role_redirect_view, home_view, order_list, register_view
from .admin_view.order_view import order_detail, order_cancel_status, order_confirm_status
from .user_view.category import category_view
from .user_view.category import category_detail_view
from .user_view.category import product_detail_user
from .user_view.add_to_cart import add_to_cart
from .admin_view.sanpham import product_list
from .admin_view.chitietsanpham import product_detail
from .authen_view import register_view, login_view, logout_view, role_redirect_view, order_list
from .admin_view.order_view import order_detail, order_cancel_status, order_confirm_status
from .user_view.category import category_view, category_detail_view, product_detail_user
from .user_view.add_to_cart import add_to_cart
from .user_view.cart import cart
from .user_view.order import order
from .user_view.donhang import donhang
from .user_view.buy_now import buy_now
