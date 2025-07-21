from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')

def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'total': product.price * cart[str(product.id)]
        })
    return render(request, 'store/cart.html', {'cart_items': cart_items})

@login_required
def process_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')
    order = Order.objects.create(user=request.user)
    for product_id, quantity in cart.items():
        product = Product.objects.get(pk=product_id)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)
    request.session['cart'] = {}  # clear cart after order
    return render(request, 'store/order_success.html', {'order': order})
