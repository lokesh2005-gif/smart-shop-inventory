from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'someap'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/add-stock/', views.add_stock, name='add_stock'),
    path('products/<int:pk>/subtract-stock/', views.subtract_stock, name='subtract_stock'),

    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('reports/low-stock/', views.LowStockReportView.as_view(), name='low_stock_report'),

    # Authentication
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='someap/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
