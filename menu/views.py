from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Food, Category, Order, OrderItem


from .models import (
    Food, Category, Cart, CartItem,
    Rating, Order, OrderItem
)


def home(request):
    foods = Food.objects.filter(is_available=True)
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        foods = foods.filter(name__icontains=query)

    food_type = request.GET.get('type')
    if food_type:
        foods = foods.filter(food_type=food_type)

    return render(request, 'menu/home.html', {
        'foods': foods,
        'categories': categories
    })


def food_detail(request, id):
    food = get_object_or_404(Food, id=id)
    return render(request, 'menu/food_detail.html', {'food': food})


def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    foods = Food.objects.filter(category=category, is_available=True)

    return render(request, 'menu/category.html', {
        'category': category,
        'foods': foods
    })


def special_offers(request):
    specials = Food.objects.filter(is_special=True, is_available=True)
    return render(request, 'menu/special_offers.html', {'specials': specials})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'menu/signup.html', {'form': form})


@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.food.price * item.quantity for item in items)

    return render(request, 'menu/cart.html', {
        'items': items,
        'total': total
    })


@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        food=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )
    item.delete()
    return redirect('cart')


@login_required
def rate_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    if request.method == "POST":
        stars = int(request.POST.get('stars'))

        Rating.objects.update_or_create(
            user=request.user,
            food=food,
            defaults={'stars': stars}
        )

    return redirect('food_detail', id=food.id)


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items.exists():
        return redirect('home')

    order = Order.objects.create(user=request.user)

    for item in items:
        OrderItem.objects.create(
            order=order,
            food=item.food,
            quantity=item.quantity
        )

    items.delete()  # clear cart after checkout

    return render(request, 'menu/checkout_success.html', {
        'order': order
    })

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    foods = Food.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for food in foods:
        qty = cart.get(str(food.id), 0)
        item_total = food.price * qty
        total += item_total

        cart_items.append({
            'food': food,
            'qty': qty,
            'total': item_total
        })

    return render(request, 'menu/cart.html', {
        'cart_items': cart_items,
        'total': total
    })
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home')

    order = Order.objects.create(user=request.user)

    for food_id, qty in cart.items():
        food = get_object_or_404(Food, id=food_id)
        OrderItem.objects.create(
            order=order,
            food=food,
            quantity=qty
        )

    request.session['cart'] = {}  # clear cart after checkout

    return render(request, 'menu/checkout_success.html', {
        'order': order
    })  

@login_required
def add_to_cart(request, food_id):
    cart = request.session.get('cart', {})
    cart[str(food_id)] = cart.get(str(food_id), 0) + 1
    request.session['cart'] = cart
    return redirect('home')
@login_required
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
    return redirect('cart')
@login_required
def rate_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    if request.method == "POST":
        stars = int(request.POST.get('stars'))

        Rating.objects.update_or_create(
            user=request.user,
            food=food,
            defaults={'stars': stars}
        )

    return redirect('food_detail', id=food.id)


