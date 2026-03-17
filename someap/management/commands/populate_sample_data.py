import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from someap.models import Category, Product

class Command(BaseCommand):
    help = 'Populate the database with sample categories and products'

    def handle(self, *args, **kwargs):
        data = {
            "Fruits & Vegetables": [
                "Tomato", "Potato", "Onion", "Carrot", "Cabbage", "Cauliflower",
                "Brinjal", "Green Chili", "Capsicum", "Cucumber", "Beetroot",
                "Radish", "Spinach", "Coriander Leaves", "Mint Leaves", "Apple",
                "Banana", "Orange", "Mango", "Grapes", "Pineapple", "Papaya",
                "Watermelon", "Pomegranate", "Lemon"
            ],
            "Dairy Products": [
                "Milk", "Curd", "Butter", "Paneer", "Cheese Slices", "Cheese Cubes",
                "Yogurt", "Fresh Cream", "Buttermilk", "Ghee", "Flavoured Milk",
                "Condensed Milk", "Milk Powder", "Greek Yogurt", "Lassi",
                "Chocolate Milk", "Strawberry Yogurt", "Vanilla Yogurt",
                "Cooking Cream", "Salted Butter"
            ],
            "Beverages": [
                "Tea Powder", "Coffee Powder", "Instant Coffee", "Green Tea",
                "Lemon Tea", "Cola Soft Drink", "Orange Soft Drink", "Lemon Soda",
                "Mango Juice", "Apple Juice", "Mixed Fruit Juice", "Coconut Water",
                "Energy Drink", "Sports Drink", "Iced Tea", "Chocolate Drink Powder",
                "Malt Drink Powder", "Drinking Water Bottle", "Soda Water", "Cold Coffee"
            ],
            "Snacks": [
                "Potato Chips", "Banana Chips", "Nachos", "Popcorn", "Cheese Balls",
                "Masala Peanuts", "Roasted Peanuts", "Mixture Namkeen", "Murukku",
                "Chakli", "Biscuits", "Cream Biscuits", "Chocolate Biscuits",
                "Crackers", "Wafers", "Pretzels", "Corn Puffs", "Energy Bars",
                "Granola Bars", "Trail Mix", "Salted Cashews", "Almond Snack Pack",
                "Peanut Butter Cookies", "Oat Cookies", "Rice Crackers"
            ],
            "Grains & Rice": [
                "Basmati Rice", "Raw Rice", "Brown Rice", "Idli Rice", "Wheat Flour",
                "Maida Flour", "Rava (Semolina)", "Corn Flour", "Oats", "Barley",
                "Millet", "Quinoa", "Poha", "Vermicelli", "Pasta", "Macaroni",
                "Noodles", "Whole Wheat Pasta", "Multigrain Flour", "Rice Flour"
            ],
            "Cooking Essentials": [
                "Cooking Oil", "Sunflower Oil", "Groundnut Oil", "Olive Oil",
                "Mustard Oil", "Salt", "Sugar", "Brown Sugar", "Jaggery",
                "Turmeric Powder", "Red Chili Powder", "Coriander Powder",
                "Garam Masala", "Cumin Seeds", "Mustard Seeds", "Fenugreek Seeds",
                "Tamarind", "Baking Powder", "Baking Soda", "Vinegar"
            ],
            "Personal Care": [
                "Bath Soap", "Liquid Hand Wash", "Shampoo", "Conditioner",
                "Hair Oil", "Toothpaste", "Toothbrush", "Face Wash", "Face Cream",
                "Body Lotion", "Deodorant", "Shaving Cream", "Razor", "Talcum Powder",
                "Sunscreen Lotion", "Lip Balm", "Hand Sanitizer", "Wet Wipes",
                "Cotton Buds", "Bath Sponge"
            ],
            "Household Items": [
                "Dishwash Liquid", "Dishwash Bar", "Floor Cleaner", "Toilet Cleaner",
                "Glass Cleaner", "Detergent Powder", "Detergent Liquid",
                "Fabric Softener", "Garbage Bags", "Tissue Paper", "Paper Towels",
                "Aluminum Foil", "Plastic Wrap", "Scrub Sponge", "Broom", "Mop",
                "Bucket", "Dustpan", "Air Freshener", "Mosquito Repellent"
            ],
            "Bakery Items": [
                "White Bread", "Brown Bread", "Multigrain Bread", "Buns",
                "Burger Buns", "Sandwich Bread", "Cupcakes", "Chocolate Cake",
                "Vanilla Cake", "Cookies", "Muffins", "Donuts", "Croissant",
                "Garlic Bread", "Fruit Cake"
            ],
            "Frozen Foods": [
                "Frozen Peas", "Frozen Corn", "Frozen Mixed Vegetables",
                "Frozen French Fries", "Frozen Nuggets", "Frozen Fish Fillet",
                "Frozen Chicken", "Frozen Paratha", "Frozen Pizza",
                "Ice Cream Vanilla", "Ice Cream Chocolate", "Ice Cream Strawberry",
                "Ice Cream Mango", "Frozen Paneer Cubes", "Frozen Sweet Corn"
            ]
        }

        today = timezone.now().date()
        
        self.stdout.write(self.style.SUCCESS("Starting to populate sample data..."))
        
        for category_name, products in data.items():
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={"description": f"All {category_name.lower()}"}
            )
            
            if created:
                 self.stdout.write(self.style.SUCCESS(f"Created category: {category_name}"))
                 
            for product_name in products:
                # Randomize data for a realistic look
                price = round(random.uniform(10.0, 500.0), 2)
                quantity = random.randint(0, 200)
                low_stock = random.randint(5, 30)
                
                # Assign some products expiring soon (within 7 days), some expired, some safe
                days_offset = random.choice([-5, -1, 3, 5, 20, 60, 100])
                expiry_date = today + timedelta(days=days_offset)
                manufacture_date = today - timedelta(days=random.randint(30, 365))
                
                # Correct the expiry constraint if random selection breaks it
                if expiry_date <= manufacture_date:
                    expiry_date = manufacture_date + timedelta(days=180)
                
                weight_vol = random.choice(["500g", "1kg", "1L", "250g", "2L", "100ml"])

                Product.objects.get_or_create(
                    product_name=product_name,
                    category=category,
                    defaults={
                        "price": price,
                        "quantity": quantity,
                        "low_stock_limit": low_stock,
                        "manufacture_date": manufacture_date,
                        "expiry_date": expiry_date,
                        "brand": "Sample Brand",
                        "weight_or_volume": weight_vol,
                        "barcode": f"890{random.randint(100000000, 999999999)}",
                        "description": f"High quality {product_name.lower()}."
                    }
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated sample data!"))
