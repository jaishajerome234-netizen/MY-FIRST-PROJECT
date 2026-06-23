import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodorder.settings')
django.setup()

from menu.models import Category, MenuItem
from django.contrib.auth.models import User

# Admin user
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin created: admin / admin123")

categories = [
    ('Burgers', '🍔'),
    ('Pizza', '🍕'),
    ('Biryani', '🍛'),
    ('Drinks', '🥤'),
    ('Desserts', '🍰'),
    ('Salads', '🥗'),
]
cats = {}
for name, icon in categories:
    cat, _ = Category.objects.get_or_create(name=name, defaults={'icon': icon})
    cats[name] = cat

items = [
    ('Classic Beef Burger', 'Juicy beef patty with lettuce, tomato, and our signature sauce', 199, 'Burgers', True, False),
    ('Chicken BBQ Burger', 'Grilled chicken with smoky BBQ sauce and crispy onions', 179, 'Burgers', True, False),
    ('Veggie Delight Burger', 'Crispy veggie patty loaded with fresh veggies', 149, 'Burgers', False, True),
    ('Margherita Pizza', 'Classic tomato sauce, fresh mozzarella and basil', 249, 'Pizza', True, True),
    ('Pepperoni Pizza', 'Loaded with premium pepperoni and melted cheese', 299, 'Pizza', True, False),
    ('Chicken Tikka Pizza', 'Indian-spiced chicken tikka on a tangy tomato base', 279, 'Pizza', False, False),
    ('Hyderabadi Chicken Biryani', 'Aromatic basmati rice cooked with tender chicken and spices', 199, 'Biryani', True, False),
    ('Veg Dum Biryani', 'Fragrant basmati with seasonal vegetables and whole spices', 169, 'Biryani', False, True),
    ('Mango Lassi', 'Chilled yoghurt blended with fresh Alphonso mango', 79, 'Drinks', False, True),
    ('Cold Coffee', 'Creamy cold coffee with a hint of chocolate', 89, 'Drinks', False, True),
    ('Fresh Lime Soda', 'Refreshing lime with soda and a pinch of salt', 49, 'Drinks', False, True),
    ('Chocolate Lava Cake', 'Warm chocolate cake with a gooey molten center', 129, 'Desserts', False, True),
    ('Gulab Jamun', 'Soft milk-solid balls soaked in rose-flavoured sugar syrup', 79, 'Desserts', False, True),
    ('Caesar Salad', 'Crisp romaine, croutons, parmesan and classic Caesar dressing', 149, 'Salads', False, True),
]

for name, desc, price, cat_name, popular, veg in items:
    MenuItem.objects.get_or_create(name=name, defaults={
        'description': desc, 'price': price, 'category': cats[cat_name],
        'is_popular': popular, 'is_vegetarian': veg, 'is_available': True
    })

print(f"Seeded {MenuItem.objects.count()} menu items across {Category.objects.count()} categories.")
