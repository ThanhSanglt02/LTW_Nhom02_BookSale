from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booksale_app.models import (
    Customer, Employee, Genre, Category, Publisher, Product, 
    Genre_Item, Order, Order_Item, Cart, Cart_Item
)
from decimal import Decimal
from datetime import date


class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu và superuser admin'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bắt đầu tạo dữ liệu mẫu...'))

        # Tạo superuser admin
        self.create_superuser()
        
        # Tạo dữ liệu mẫu
        self.create_sample_data()
        
        self.stdout.write(self.style.SUCCESS('Hoàn thành tạo dữ liệu mẫu!'))

    def create_superuser(self):
        """Tạo superuser admin nếu chưa tồn tại"""
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" đã tồn tại, bỏ qua...'))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Đã tạo superuser: {username} / {password}'))

    def create_sample_data(self):
        """Tạo dữ liệu mẫu"""
        
        # Tạo Genre
        genre1, _ = Genre.objects.get_or_create(
            genre_name='Văn học',
            defaults={'description': 'Thể loại văn học'}
        )
        genre2, _ = Genre.objects.get_or_create(
            genre_name='Giáo trình',
            defaults={'description': 'Sách giáo trình'}
        )
        genre3, _ = Genre.objects.get_or_create(
            genre_name='Thiếu nhi',
            defaults={'description': 'Sách thiếu nhi'}
        )
        
        # Tạo Category
        category1, _ = Category.objects.get_or_create(
            category_name='Sách giáo trình',
            defaults={'description': 'Danh mục sách giáo trình'}
        )
        category2, _ = Category.objects.get_or_create(
            category_name='Sách văn học',
            defaults={'description': 'Danh mục sách văn học'}
        )
        category3, _ = Category.objects.get_or_create(
            category_name='Sách thiếu nhi',
            defaults={'description': 'Danh mục sách thiếu nhi'}
        )
        
        # Tạo Publisher
        publisher1, _ = Publisher.objects.get_or_create(
            publisher_name='NXB Đại Học Quốc Gia Hà Nội',
            defaults={'email': 'nxb@vnu.edu.vn'}
        )
        publisher2, _ = Publisher.objects.get_or_create(
            publisher_name='NXB Giáo Dục',
            defaults={'email': 'nxb@moet.gov.vn'}
        )
        publisher3, _ = Publisher.objects.get_or_create(
            publisher_name='NXB Kim Đồng',
            defaults={'email': 'nxb@kimdong.com.vn'}
        )
        
        # Tạo Product
        products_data = [
            {
                'product_name': 'Sách quản trị học',
                'description': 'Giáo trình quản trị học đại cương',
                'cost_price': Decimal('10000'),
                'sell_price': Decimal('15000'),
                'quantity': 50,
                'publisher': publisher1,
                'category': category1,
                'genres': [genre2]
            },
            {
                'product_name': 'Tắt đèn',
                'description': 'Tiểu thuyết nổi tiếng của Ngô Tất Tố',
                'cost_price': Decimal('12000'),
                'sell_price': Decimal('15000'),
                'quantity': 30,
                'publisher': publisher2,
                'category': category2,
                'genres': [genre1]
            },
            {
                'product_name': 'Truyện Kiều',
                'description': 'Tác phẩm kinh điển của Nguyễn Du',
                'cost_price': Decimal('13000'),
                'sell_price': Decimal('15000'),
                'quantity': 40,
                'publisher': publisher2,
                'category': category2,
                'genres': [genre1]
            },
            {
                'product_name': 'Chí Phèo',
                'description': 'Truyện ngắn nổi tiếng của Nam Cao',
                'cost_price': Decimal('11000'),
                'sell_price': Decimal('15000'),
                'quantity': 35,
                'publisher': publisher2,
                'category': category2,
                'genres': [genre1]
            },
            {
                'product_name': 'Thiết học Mác-Lênin',
                'description': 'Giáo trình triết học Mác-Lênin',
                'cost_price': Decimal('10000'),
                'sell_price': Decimal('15000'),
                'quantity': 60,
                'publisher': publisher1,
                'category': category1,
                'genres': [genre2]
            },
            {
                'product_name': 'Tư tưởng Hồ Chí Minh',
                'description': 'Giáo trình tư tưởng Hồ Chí Minh',
                'cost_price': Decimal('10000'),
                'sell_price': Decimal('15000'),
                'quantity': 55,
                'publisher': publisher1,
                'category': category1,
                'genres': [genre2]
            },
            {
                'product_name': 'Kinh tế học vi mô',
                'description': 'Giáo trình kinh tế học vi mô',
                'cost_price': Decimal('12000'),
                'sell_price': Decimal('15000'),
                'quantity': 45,
                'publisher': publisher1,
                'category': category1,
                'genres': [genre2]
            },
        ]
        
        for product_data in products_data:
            genres = product_data.pop('genres')
            product, created = Product.objects.get_or_create(
                product_name=product_data['product_name'],
                defaults=product_data
            )
            if created:
                # Thêm genres cho product
                for genre in genres:
                    Genre_Item.objects.get_or_create(
                        product=product,
                        genre=genre
                    )
                self.stdout.write(self.style.SUCCESS(f'✓ Đã tạo sản phẩm: {product.product_name}'))
        
        self.stdout.write(self.style.SUCCESS('✓ Đã tạo dữ liệu mẫu thành công!'))

