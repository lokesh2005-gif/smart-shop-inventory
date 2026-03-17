from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Product, StockTransaction

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['transaction_type', 'quantity', 'notes']
        widgets = {
            'transaction_type': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Quantity', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'textarea', 'rows': 2, 'placeholder': 'Optional notes'}),
        }

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        transaction_type = self.cleaned_data.get('transaction_type')
        
        if quantity and quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero.')
            
        if self.product and transaction_type == 'SUBTRACT':
            if self.product.quantity < quantity:
                raise forms.ValidationError(f'Not enough stock. Current stock is {self.product.quantity}.')
                
        return quantity

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'brand', 'price', 'quantity', 'low_stock_limit', 
                  'product_image', 'manufacture_date', 'expiry_date', 'barcode', 'weight_or_volume']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Product Name'}),
            'category': forms.Select(attrs={'class': 'select'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'rows': 3, 'placeholder': 'Product Description'}),
            'brand': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Brand (Optional)'}),
            'price': forms.NumberInput(attrs={'class': 'input', 'step': '0.01', 'placeholder': 'Price'}),
            'quantity': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Stock Quantity'}),
            'low_stock_limit': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Low Stock Alert Level'}),
            'product_image': forms.FileInput(attrs={'class': 'input', 'accept': 'image/*'}),
            'manufacture_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'barcode': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Barcode (Optional)'}),
            'weight_or_volume': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Weight/Volume (e.g., 500g, 1L)'}),
        }

    def clean_product_image(self):
        image = self.cleaned_data.get('product_image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size must not exceed 5MB.')
            # Check file type
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            file_extension = image.name.split('.')[-1].lower()
            if file_extension not in valid_extensions:
                raise forms.ValidationError(f'Invalid image format. Allowed: {", ".join(valid_extensions)}')
        return image

    def clean(self):
        cleaned_data = super().clean()
        expiry_date = cleaned_data.get('expiry_date')
        manufacture_date = cleaned_data.get('manufacture_date')
        
        # Validate that expiry date is after manufacture date
        if manufacture_date and expiry_date:
            if expiry_date <= manufacture_date:
                raise forms.ValidationError('Expiry date must be after manufacture date.')
        
        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'textarea'}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'password1': forms.PasswordInput(attrs={'class': 'input'}),
            'password2': forms.PasswordInput(attrs={'class': 'input'}),
        }
