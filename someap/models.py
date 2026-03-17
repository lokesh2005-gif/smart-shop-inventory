from django.db import models


class Category(models.Model):
    """A category for products."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db import models
import os

class Product(models.Model):
    product_name = models.CharField(max_length=200, default='Unnamed Product')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    quantity = models.PositiveIntegerField(default=0)
    low_stock_limit = models.PositiveIntegerField(default=5)
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    manufacture_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    weight_or_volume = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['product_name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.product_name} ({self.category})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_limit

    @property
    def total_value(self):
        return float(self.price) * self.quantity

    @property
    def expiry_status(self):
        if self.expiry_date:
            today = timezone.now().date()
            if self.expiry_date < today:
                return 'expired'
            elif (self.expiry_date - today).days <= 7:
                return 'expiring_soon'
            else:
                return 'safe'
        return 'n/a'

class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('ADD', 'Add Stock'),
        ('SUBTRACT', 'Subtract Stock'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} for {self.product.product_name}"
