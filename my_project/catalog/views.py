from .models import Product, Category
from django.shortcuts import render, get_object_or_404, redirect
from reviews.models import Review
from django.contrib.auth.models import User 
from reviews.forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home_page(request):
    return render(request, 'catalog/home.html')

def product_list(request):
    category_id = request.GET.get('category')
    categories_db = Category.objects.all()
    
    if category_id:
        products_db = Product.objects.filter(category_id=category_id)
    else:
        products_db = Product.objects.all()
    
    context = {
        'products': products_db,
        'categories': categories_db,
        'selected_category': category_id,
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    
    form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }
    
    return render(request, 'catalog/product_detail.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'product_id': product.id,
            'title': product.title,
            'price': float(product.price),
            'quantity': 1,
            'image_path': product.image_path,
        }
    
    request.session['cart'] = cart
    request.session.modified = True
    
    messages.success(request, f'Товар "{product.title}" добавлен в корзину')
    
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

def cart_view(request):
    cart = request.session.get('cart', {})
    
    cart_items = []
    total_price = 0
    
    for item_id, item_data in cart.items():
        item_total = item_data['price'] * item_data['quantity']
        total_price += item_total
        
        cart_items.append({
            'id': item_id,
            'title': item_data['title'],
            'price': item_data['price'],
            'quantity': item_data['quantity'],
            'total': item_total,
            'image_path': item_data.get('image_path')
        })
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': sum(item['quantity'] for item in cart_items)
    }
    
    return render(request, 'catalog/cart.html', context)

def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    
    messages.info(request, 'Êîðçèíà î÷èùåíà')
    
    return redirect('catalog:cart_view')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product_title = cart[product_id_str]['title']
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'Товар "{product_title}" удален из корзины')
    
    return redirect('catalog:cart_view')

def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            if quantity > 0:
                cart[product_id_str]['quantity'] = quantity
                request.session['cart'] = cart
                request.session.modified = True
            else:
                return remove_from_cart(request, product_id)
    
    return redirect('catalog:cart_view')

def toggle_theme(request):
    response = redirect(request.META.get('HTTP_REFERER', 'product_list'))
    
    current_theme = request.COOKIES.get('theme', 'light')
    
    if current_theme == 'dark':
        response.set_cookie('theme', 'light', max_age=31536000)
    else:
        response.set_cookie('theme', 'dark', max_age=31536000)
    
    return response

@login_required
def chat_room(request, room_name):
    context = {
        'room_name': room_name,
    }
    return render(request, 'catalog/chat.html', context)