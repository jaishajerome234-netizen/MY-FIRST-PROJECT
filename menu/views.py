from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Category, MenuItem, Order, OrderItem

# ── Cart helpers (session-based) ──────────────────────────────────────────────
def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

# ── Public views ──────────────────────────────────────────────────────────────
def home(request):
    categories = Category.objects.prefetch_related('items').all()
    popular = MenuItem.objects.filter(is_popular=True, is_available=True)[:6]
    return render(request, 'menu/home.html', {'categories': categories, 'popular': popular})

def menu_list(request):
    categories = Category.objects.prefetch_related('items').all()
    selected_cat = request.GET.get('category')
    items = MenuItem.objects.filter(is_available=True)
    if selected_cat:
        items = items.filter(category__id=selected_cat)
    return render(request, 'menu/menu.html', {
        'categories': categories,
        'items': items,
        'selected_cat': int(selected_cat) if selected_cat else None,
    })

def item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk, is_available=True)
    return render(request, 'menu/item_detail.html', {'item': item})

# ── Cart views ────────────────────────────────────────────────────────────────
def cart_view(request):
    cart = get_cart(request)
    cart_items = []
    total = 0
    for item_id, qty in cart.items():
        try:
            item = MenuItem.objects.get(pk=item_id)
            subtotal = item.price * qty
            total += subtotal
            cart_items.append({'item': item, 'qty': qty, 'subtotal': subtotal})
        except MenuItem.DoesNotExist:
            pass
    return render(request, 'menu/cart.html', {'cart_items': cart_items, 'total': total})

@require_POST
def add_to_cart(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    cart = get_cart(request)
    key = str(pk)
    cart[key] = cart.get(key, 0) + 1
    save_cart(request, cart)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        count = sum(cart.values())
        return JsonResponse({'success': True, 'cart_count': count, 'message': f'{item.name} added!'})
    messages.success(request, f'"{item.name}" added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'menu_list'))

@require_POST
def update_cart(request, pk):
    cart = get_cart(request)
    key = str(pk)
    qty = int(request.POST.get('qty', 1))
    if qty <= 0:
        cart.pop(key, None)
    else:
        cart[key] = qty
    save_cart(request, cart)
    return redirect('cart')

@require_POST
def remove_from_cart(request, pk):
    cart = get_cart(request)
    cart.pop(str(pk), None)
    save_cart(request, cart)
    messages.info(request, 'Item removed from cart.')
    return redirect('cart')

# ── Checkout & Orders ─────────────────────────────────────────────────────────
@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    cart_items = []
    total = 0
    for item_id, qty in cart.items():
        try:
            item = MenuItem.objects.get(pk=item_id)
            subtotal = item.price * qty
            total += subtotal
            cart_items.append({'item': item, 'qty': qty, 'subtotal': subtotal})
        except MenuItem.DoesNotExist:
            pass
    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()
        notes = request.POST.get('notes', '')
        if not address or not phone:
            messages.error(request, 'Please fill in all required fields.')
        else:
            order = Order.objects.create(
                user=request.user,
                delivery_address=address,
                phone=phone,
                notes=notes,
                total_price=total,
            )
            for item_id, qty in cart.items():
                try:
                    item = MenuItem.objects.get(pk=item_id)
                    OrderItem.objects.create(order=order, menu_item=item, quantity=qty, price=item.price)
                except MenuItem.DoesNotExist:
                    pass
            save_cart(request, {})
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('order_success', pk=order.pk)
    return render(request, 'menu/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'menu/order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'menu/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'menu/order_detail.html', {'order': order})

# ── Auth ──────────────────────────────────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.username}!')
        return redirect('home')
    return render(request, 'menu/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.username}!')
        return redirect(request.GET.get('next', 'home'))
    return render(request, 'menu/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
