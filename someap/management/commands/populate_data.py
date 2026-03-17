from django.core.management.base import BaseCommand
from someap.models import Category, Product
import random

class Command(BaseCommand):
    help = 'Populate database with sample categories and products'

    def handle(self, *args, **options):
        # Create 10 categories
        categories_data = [
            {'name': 'Fruits', 'description': 'Fresh fruits and produce'},
            {'name': 'Vegetables', 'description': 'Fresh vegetables and greens'},
            {'name': 'Dairy', 'description': 'Milk, cheese, and dairy products'},
            {'name': 'Bakery', 'description': 'Bread, cakes, and baked goods'},
            {'name': 'Meat', 'description': 'Fresh and processed meats'},
            {'name': 'Seafood', 'description': 'Fish and seafood products'},
            {'name': 'Beverages', 'description': 'Drinks and beverages'},
            {'name': 'Snacks', 'description': 'Chips, candies, and snacks'},
            {'name': 'Canned Goods', 'description': 'Canned and preserved foods'},
            {'name': 'Household', 'description': 'Cleaning and household items'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Sample products for each category
        products_data = {
            'Fruits': [
                'Apple', 'Banana', 'Orange', 'Grapes', 'Strawberry', 'Mango', 'Pineapple', 'Watermelon',
                'Kiwi', 'Pear', 'Peach', 'Plum', 'Cherry', 'Lemon', 'Lime', 'Avocado', 'Blueberry', 'Raspberry'
            ],
            'Vegetables': [
                'Tomato', 'Potato', 'Onion', 'Carrot', 'Broccoli', 'Spinach', 'Lettuce', 'Cucumber',
                'Bell Pepper', 'Zucchini', 'Eggplant', 'Cauliflower', 'Green Beans', 'Peas', 'Corn', 'Mushroom', 'Garlic', 'Ginger'
            ],
            'Dairy': [
                'Milk', 'Cheese', 'Yogurt', 'Butter', 'Cream', 'Ice Cream', 'Cottage Cheese', 'Sour Cream',
                'Mozzarella', 'Cheddar', 'Parmesan', 'Greek Yogurt', 'Whipped Cream', 'Milk Powder', 'Cream Cheese', 'Feta'
            ],
            'Bakery': [
                'White Bread', 'Whole Wheat Bread', 'Croissant', 'Bagel', 'Muffin', 'Donut', 'Cake', 'Cookie',
                'Pie', 'Brownie', 'Pasta', 'Pizza Dough', 'Tortilla', 'Pita Bread', 'English Muffin', 'Scone'
            ],
            'Meat': [
                'Chicken Breast', 'Ground Beef', 'Pork Chops', 'Bacon', 'Sausage', 'Turkey', 'Lamb', 'Salmon',
                'Tuna Steak', 'Shrimp', 'Crab', 'Lobster', 'Beef Steak', 'Pork Tenderloin', 'Chicken Thigh', 'Turkey Bacon'
            ],
            'Seafood': [
                'Salmon Fillet', 'Tuna', 'Shrimp', 'Crab Legs', 'Lobster Tail', 'Cod', 'Halibut', 'Mahi Mahi',
                'Swordfish', 'Clams', 'Mussels', 'Oysters', 'Scallops', 'Tilapia', 'Catfish', 'Sardines'
            ],
            'Beverages': [
                'Coca Cola', 'Pepsi', 'Orange Juice', 'Apple Juice', 'Coffee', 'Tea', 'Water', 'Milk',
                'Energy Drink', 'Sports Drink', 'Beer', 'Wine', 'Soda', 'Lemonade', 'Iced Tea', 'Hot Chocolate'
            ],
            'Snacks': [
                'Potato Chips', 'Chocolate Bar', 'Candy', 'Popcorn', 'Pretzels', 'Nuts', 'Granola Bar', 'Crackers',
                'Cookies', 'Ice Cream Bar', 'Chewing Gum', 'Trail Mix', 'Rice Cakes', 'Fruit Snacks', 'Yogurt Covered Raisins', 'Beef Jerky'
            ],
            'Canned Goods': [
                'Tomato Sauce', 'Beans', 'Tuna', 'Soup', 'Vegetables', 'Fruit', 'Peanut Butter', 'Olive Oil',
                'Mayonnaise', 'Mustard', 'Ketchup', 'Pickles', 'Olives', 'Corn', 'Peas', 'Carrots'
            ],
            'Household': [
                'Dish Soap', 'Laundry Detergent', 'Toilet Paper', 'Paper Towels', 'Trash Bags', 'Cleaning Spray', 'Bleach', 'Fabric Softener',
                'Dishwasher Detergent', 'All-Purpose Cleaner', 'Glass Cleaner', 'Floor Cleaner', 'Air Freshener', 'Sponges', 'Broom', 'Mop'
            ]
        }

        # Create products
        total_products = 0
        for category in categories:
            products = products_data.get(category.name, [])
            for product_name in products:
                # Random price between $0.50 and $50
                price = round(random.uniform(0.5, 50.0), 2)
                # Random quantity between 0 and 100
                quantity = random.randint(0, 100)
                # Random low stock limit between 1 and 10
                low_stock_limit = random.randint(1, 10)

                product, created = Product.objects.get_or_create(
                    name=product_name,
                    category=category,
                    defaults={
                        'price': price,
                        'quantity': quantity,
                        'low_stock_limit': low_stock_limit
                    }
                )
                if created:
                    total_products += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(categories)} categories and {total_products} products'))
