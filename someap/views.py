from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q, Sum
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    DetailView,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
import json

from .forms import CategoryForm, ProductForm, SignUpForm, StockTransactionForm
from .models import Category, Product, StockTransaction


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'someap/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = Product.objects.count()
        context['total_categories'] = Category.objects.count()
        context['low_stock_products'] = Product.objects.filter(quantity__lte=F('low_stock_limit')).order_by('quantity')
        context['low_stock_count'] = context['low_stock_products'].count()
        context['total_inventory_value'] = Product.objects.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
        context['recent_products'] = Product.objects.order_by('-created_at')[:5]

        # Expiry Logic
        today = timezone.now().date()
        seven_days_later = today + timezone.timedelta(days=7)
        context['expiring_soon_products'] = Product.objects.filter(expiry_date__gt=today, expiry_date__lte=seven_days_later)
        context['expired_products'] = Product.objects.filter(expiry_date__lt=today)
        context['expiring_soon_count'] = context['expiring_soon_products'].count()
        context['expired_count'] = context['expired_products'].count()

        # Chart Data
        category_labels = []
        category_data = []
        for cat in Category.objects.all():
            total_qty = Product.objects.filter(category=cat).aggregate(total=Sum('quantity'))['total'] or 0
            category_labels.append(cat.name)
            category_data.append(total_qty)

        context['chart_labels'] = json.dumps(category_labels)
        context['chart_data'] = json.dumps(category_data)

        return context


@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'someap/product_list.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category')
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        if search:
            queryset = queryset.filter(
                Q(product_name__icontains=search) |
                Q(category__name__icontains=search) |
                Q(brand__icontains=search) |
                Q(barcode__icontains=search)
            )
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'someap/product_form.html'
    success_url = reverse_lazy('someap:product_list')


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'someap/product_form.html'
    success_url = reverse_lazy('someap:product_list')


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'someap/product_confirm_delete.html'
    success_url = reverse_lazy('someap:product_list')


@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'someap/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = self.object.stock_transactions.all()
        return context


@login_required
def add_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = StockTransactionForm(request.POST, product=product)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.transaction_type = 'ADD'
            transaction.save()
            product.quantity += transaction.quantity
            product.save()
            messages.success(request, f'Added {transaction.quantity} units to {product.product_name}.')
            return redirect('someap:product_detail', pk=product.pk)
    else:
        form = StockTransactionForm(initial={'transaction_type': 'ADD'})

    return render(request, 'someap/stock_form.html', {'form': form, 'product': product, 'action': 'Add'})


@login_required
def subtract_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = StockTransactionForm(request.POST, product=product)
        form.instance.transaction_type = 'SUBTRACT'
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.transaction_type = 'SUBTRACT'
            transaction.save()
            product.quantity -= transaction.quantity
            product.save()
            messages.success(request, f'Subtracted {transaction.quantity} units from {product.product_name}.')
            return redirect('someap:product_detail', pk=product.pk)
    else:
        form = StockTransactionForm(initial={'transaction_type': 'SUBTRACT'})

    return render(request, 'someap/stock_form.html', {'form': form, 'product': product, 'action': 'Subtract'})


@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'someap/category_list.html'
    context_object_name = 'categories'


@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'someap/category_form.html'
    success_url = reverse_lazy('someap:category_list')


@method_decorator(login_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'someap/category_form.html'
    success_url = reverse_lazy('someap:category_list')


@method_decorator(login_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'someap/category_confirm_delete.html'
    success_url = reverse_lazy('someap:category_list')


@method_decorator(login_required, name='dispatch')
class LowStockReportView(ListView):
    model = Product
    template_name = 'someap/low_stock_report.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(quantity__lte=F('low_stock_limit')).order_by('quantity')


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'someap/signup.html'
    success_url = reverse_lazy('someap:dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
