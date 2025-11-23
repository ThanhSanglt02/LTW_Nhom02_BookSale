from django.db import models
from django.contrib import auth 


# Create your models here
class Customer(models.Model):
    user = models.OneToOneField(auth.get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
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
    avatar = models.ImageField(upload_to='customers/', null=True, blank=True)
    create_at = models.DateTimeField(
        verbose_name = "Ngày tạo",
        auto_now_add=True
    )
    def __str__(self):
        return self.cust_name
    
class Employee(models.Model):
    user = models.OneToOneField(auth.get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    emp_name = models.CharField(
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
    def __str__(self):
        return self.emp_name

class Genre(models.Model):
    genre_name = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Tên thể loại"
    )
    description = models.TextField(
        blank=False, null=False,
        help_text = "Mô tả thể loại"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return self.genre_name
    
class Category(models.Model):
    category_name = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Tên danh mục"
    )
    description = models.TextField(
        blank=False, null=False,
        help_text = "Mô tả"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
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
    def __str__(self):
        return self.publisher_name

class Product(models.Model):
    product_name = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Tên sản phẩm"
    )
    description = models.TextField(
        blank=False, null=False,
        help_text = "Mô tả"
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    sell_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=0)
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
    create_at = models.DateTimeField(auto_now_add=True)
    
class Cart(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
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
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    added_at = models.DateTimeField(auto_now_add=True)

class PaymentMethod(models.TextChoices):
    CASH = "cash", "Cash"
    CREDIT = "credit", "Credit Card"


class Order(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Đã xác nhận'),
        ('pending', 'Chờ xác nhận'),
        ('cancelled', 'Đã hủy'),
        ('completed', 'Hoàn thành')
    ]
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'  # mặc định là "Chờ xác nhận"
    )
    cancel_reason = models.TextField(blank=True, null=True)
    shipping_date = models.DateField(verbose_name= "Ngày giao hàng", blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(
        Customer,
        on_delete = models.PROTECT
    )
    payment_method = models.CharField(choices=PaymentMethod.choices, max_length=20)
    

class Order_Item(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete = models.PROTECT
    )
    order = models.ForeignKey(
        Order,
        on_delete = models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=0)
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
    rating = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
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
    def __str__(self):
        return self.content
    
class Supplier(models.Model):
    sup_name = models.CharField(
        max_length = 255,
        blank=False, null=False,
        help_text = "Tên nhà cung cấp"
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
    def __str__(self):
        return self.sup_name
    
class ImportOrder(models.Model):
    import_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    note = models.TextField(
        blank=False, null=False,
        help_text = "Mô tả"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    product = models.ManyToManyField(
        'Product',
        through="ImportOrder_Item")
    supplier = models.ForeignKey(
        Supplier,
        on_delete = models.PROTECT
    )
    employee = models.ForeignKey(
        Employee,
        on_delete = models.PROTECT
    )
    def __str__(self):
        # định dạng ngày giờ theo kiểu "YYYY-MM-DD HH:MM:SS"
        formatted_date = self.import_date.strftime("%Y-%m-%d %H:%M:%S")
        return f"ImportOrder #{self.id} - {formatted_date}"

class ImportOrder_Item(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete = models.PROTECT
    )
    importOrder = models.ForeignKey(
        ImportOrder,
        on_delete = models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

class ExportOrder(models.Model):
    export_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    reason = models.TextField(
        blank=False, null=False,
        help_text = "Mô tả"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    product = models.ManyToManyField(
        'Product',
        through="ExportOrder_Item")
    order = models.ForeignKey(
        Order,
        on_delete = models.PROTECT
    )
    employee = models.ForeignKey(
        Employee,
        on_delete = models.PROTECT
    )
    def __str__(self):
        # định dạng ngày giờ theo kiểu "YYYY-MM-DD HH:MM:SS"
        formatted_date = self.export_date.strftime("%Y-%m-%d %H:%M:%S")
        return f"ImportOrder #{self.id} - {formatted_date}"
    
class ExportOrder_Item(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete = models.PROTECT
    )
    exportOrder = models.ForeignKey(
        ExportOrder,
        on_delete = models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )