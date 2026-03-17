# Smart Shop Inventory App

A comprehensive Django-based inventory management system for small retail shops.

## Features

- **User Authentication**: Secure login/logout system
- **Product Management**: Add, edit, delete, and search products
- **Category Management**: Organize products into categories
- **Inventory Tracking**: Monitor stock levels and values
- **Low Stock Alerts**: Automatic notifications for products below threshold
- **Admin Dashboard**: Overview of inventory statistics
- **Reports**: Low stock and category-wise reports
- **Responsive UI**: Mobile-friendly Bootstrap interface

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone or download the project**
   ```bash
   cd path/to/project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Populate sample data** (optional)
   ```bash
   python manage.py populate_data
   ```

6. **Create superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the server**
   ```bash
   python manage.py runserver
   ```

8. **Open in browser**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### First Time Setup
1. Visit http://127.0.0.1:8000/signup/ to create an account
2. Or use the admin panel to create users

### Managing Inventory
- **Dashboard**: View overview and low stock alerts
- **Products**: Add/edit/delete products with search and filtering
- **Categories**: Organize products into categories
- **Reports**: View low stock items

### Admin Features
- Access Django admin at /admin/
- Manage users, products, and categories
- Bulk operations on products

## Project Structure

```
smart_shop_inventory/
├── someap/                    # Main app
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── forms.py              # Form definitions
│   ├── urls.py               # URL routing
│   ├── admin.py              # Admin configuration
│   ├── templates/            # HTML templates
│   └── management/           # Custom management commands
├── somept/                   # Project settings
├── static/                   # Static files (CSS, JS)
├── db.sqlite3                # Database
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## Models

### Product
- name: Product name
- category: Foreign key to Category
- price: Decimal field
- quantity: Stock quantity
- low_stock_limit: Alert threshold
- created_at/updated_at: Timestamps

### Category
- name: Category name (unique)
- description: Optional description

## Security Features

- CSRF protection on all forms
- Login required for all inventory operations
- Form validation
- Secure password handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.