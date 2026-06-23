# 🍔 FoodieRush – Django Food Ordering Website

A full-featured food ordering website built with Django.

## Features
- Browse menu by category (Burgers, Pizza, Biryani, Drinks, Desserts, Salads)
- Session-based cart with AJAX add-to-cart
- User registration & login
- Checkout with delivery address
- Order tracking with status (Pending → Confirmed → Preparing → Delivered)
- Django Admin panel to manage items, categories, and orders
- 14 pre-seeded menu items

## Quick Start

```bash
# 1. Install dependencies
pip install django pillow

# 2. Run migrations (already done if you received the db.sqlite3)
python manage.py migrate

# 3. Seed sample data (optional – already seeded)
python manage.py shell < seed_data.py

# 4. Start the server
python manage.py runserver
```

Open http://127.0.0.1:8000

## Admin Panel
URL: http://127.0.0.1:8000/admin/
Username: **admin**
Password: **admin123**

## Project Structure
```
foodorder/
├── foodorder/          # Project settings & URLs
├── menu/               # Main app
│   ├── models.py       # Category, MenuItem, Order, OrderItem
│   ├── views.py        # All views (home, menu, cart, checkout, orders, auth)
│   ├── urls.py         # URL routing
│   ├── admin.py        # Admin configuration
│   └── context_processors.py
├── templates/          # HTML templates
├── static/             # CSS & JS
├── db.sqlite3          # SQLite database (with seed data)
└── seed_data.py        # Sample data loader
```

## Pages
| URL | Description |
|-----|-------------|
| `/` | Home page with popular items |
| `/menu/` | Full menu with category filter |
| `/cart/` | Shopping cart |
| `/checkout/` | Checkout form |
| `/orders/` | My orders list |
| `/orders/<id>/` | Order detail |
| `/login/` | Login |
| `/register/` | Register |
| `/admin/` | Admin panel |
