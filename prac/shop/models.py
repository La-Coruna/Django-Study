from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=10)
    joinded_at = models.DateTimeField(auto_now_add=True)
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        to = "self",
        related_name = 'subcategories',
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock =  models.PositiveIntegerField()
    category = models.ForeignKey(
        to = Category,
        on_delete = models.CASCADE,
        related_name = "products"
    )
    
class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="cart")
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
class Order(models.Model):
    STATUS_CHOICE = [('pending',"결제 대기"), ("shipping", "배송 중"), ('completed',"배송 완료")]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    
class Payment(models.Model):
    METHOD_CHOICES = [('card','신용카드'), ('bank','계좌이체'), ('simple', '간편결제')]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    
class Review(models.Model):
    # 작성한 회원, 어떤 상품, 내용, 평점(1~5점), 작성일
    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Address(models.Model):
    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE
    )
    address_line = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    