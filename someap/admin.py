from django.contrib import admin
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from .models import Category, Product


class LowStockFilter(admin.SimpleListFilter):
    title = _('stock status')
    parameter_name = 'low_stock'

    def lookups(self, request, model_admin):
        return (
            ('low', _('Low stock')),
            ('ok', _('Sufficient stock')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(quantity__lte=F('low_stock_limit'))
        if self.value() == 'ok':
            return queryset.filter(quantity__gt=F('low_stock_limit'))
        return queryset


from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'category',
        'brand',
        'barcode',
        'price',
        'quantity',
        'low_stock_limit',
        'low_stock',
        'total_value',
        'expiry_date',
        'expiry_status',
        'product_image_thumb',
        'created_at',
        'updated_at',
    )
    list_filter = ('category', LowStockFilter, 'brand', 'expiry_date')
    search_fields = ('product_name', 'category__name', 'brand', 'barcode')
    actions = ['mark_as_restocked']

    readonly_fields = ('product_image_thumb',)

    fieldsets = (
        (None, {
            'fields': ('product_name', 'category', 'description', 'brand', 'barcode', 'price', 'quantity', 'low_stock_limit', 'weight_or_volume')
        }),
        ('Dates', {
            'fields': ('manufacture_date', 'expiry_date')
        }),
        ('Image', {
            'fields': ('product_image', 'product_image_thumb')
        }),
        ('Status', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def product_image_thumb(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:4px;" />', obj.product_image.url)
        return "-"
    product_image_thumb.short_description = 'Image'


    def low_stock(self, obj: Product) -> bool:
        return obj.is_low_stock
    low_stock.boolean = True
    low_stock.short_description = 'Low stock'

    @admin.action(description='Mark selected products as restocked')
    def mark_as_restocked(self, request, queryset):
        for product in queryset:
            # Restocking up to the defined threshold
            product.quantity = max(product.quantity, product.low_stock_limit)
            product.save()
        self.message_user(request, f'Successfully restocked {queryset.count()} product(s).')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_count')
    search_fields = ('name', 'description')

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


# Customize Django Admin Site
admin.site.site_header = 'Smart Shop Inventory'
admin.site.site_title = 'Smart Shop Inventory Admin'
admin.site.index_title = 'Welcome to Smart Shop Inventory Management'
