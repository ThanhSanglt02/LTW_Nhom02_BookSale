from django.db import models
from django.contrib import auth 
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.SET_NULL, null=True, blank=False)
    cust_name = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Tên khách hàng"
    )
    email = models.EmailField(
        max_length = 100,
        help_text = "Email"
    )
    phone = models.CharField(
        max_length = 15,
        blank=False, null=False,
        help_text = "Số điện thoại"
    )
    address = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Địa chi"
    )
    dob = models.DateField(
        verbose_name="Ngày sinh"
    )
    create_at = models.DateField(
        verbose_name = "Ngày tạo"
    )
    def __str__(self):
        return self.cust_name
    

class Genre(models.Model):
    genre_name = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Tên thể loại"
    )
    description = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Mô tả thể loại"
    )
    created_at = models.DateField(
        verbose_name="Ngày tạo"
    )
    updated_at = models.DateField(
        verbose_name = "Ngày cập nhật"
    )
    def __str__(self):
        return self.genre_name
    
class Category(models.Model):
    category_name = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Tên danh mục"
    )
    description = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Mô tả"
    )
    created_at = models.DateField(
        verbose_name="Ngày tạo"
    )
    updated_at = models.DateField(
        verbose_name = "Ngày cập nhật"
    )
    def __str__(self):
        return self.category_name
class Publisher(models.Model):
    publisher_name = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Tên nhà xuất bản"
    )
    email = models.EmailField(
        max_length = 100,
        help_text = "Email"
    )
    

class Product(models.Model):
    product_name = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Tên sản phẩm"
    )
    description = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Mô tả"
    )
    image = models.CharField(
        max_length = 150,
        help_text = "Đường dẫn hình ảnh"
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    sell_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.IntegerField()
    publisher = models.ForeignKey(
        Publisher, 
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    genre = models.ManyToManyField(
        'Genre',
        through="Genre_Item")
    cart = models.ManyToManyField(
        'Cart',
        through='Cart_Item'
    )
    order = models.ManyToManyField(
        'Order',
         through="Order_Item"
    )

    def __str__(self):
        return self.product_name
    
class Genre_Item(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE)
    # Thuộc tính role dùng dể lưu trữ thông tin bổ sung về mối quan hệ giữa lớp Book và Contributor. 
    create_at = models.DateField(
        verbose_name = "Ngày tạo"
    )
    
class Cart(models.Model):
    create_at = models.DateField(
        verbose_name = "Ngày tạo"
    )
    updated_at = models.DateField(
        verbose_name = "Ngày cập nhật"
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

class Cart_Item(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    added_at = models.DateField(
        verbose_name = "Ngày thêm"
    )

class PaymentMethod(models.Model):
    class pMethod(models.TextChoices):
        CASH = "cash", "CASH"
        CREDIT_CARD = "credit", "CREDIT_CARD"
    pMethod_name = models.CharField(
        verbose_name="The method this payment had in the order.",
        choices=pMethod.choices, max_length=20)
class Order(models.Model):
    order_date = models.DateTimeField(
        verbose_name = "Ngày đặt hàng"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    customer = models.ForeignKey(
        Customer,
        on_delete = models.PROTECT
    )
    paymentMethod = models.ForeignKey(
        PaymentMethod,
        on_delete = models.CASCADE
    )

class Order_Item(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete = models.PROTECT
    )
    order = models.ForeignKey(
        Order,
        on_delete = models.PROTECT
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(
        null=True,
        help_text="The date and time the review was last edited.")
    # Thuộc tính creator liên kết đến model của bảng dữ liệu người
    # dùng của Django ở dạng Một – Nhiều (phương thức auth.get_user_model() sẽ trả
    # về model quản lý dữ liệu người dùng này).
    creator = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="The Book that this review is for.")
