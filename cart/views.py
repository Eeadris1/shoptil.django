from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist
from django.shortcuts import render,redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required


# This function generates or retrieves a unique cart identifier associated with the user's session.
def _cart_id(request):
    # Attempt to retrieve the cart identifier from the session.
    cart = request.session.session_key

    # If cart identifier doesn't exist (session is new), create a new one.
    if not cart:
        cart = request.session.create()

    # Return the cart identifier.
    return cart


# This function adds a product to the shopping cart.
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  #this Retrieve the product object based on the provided product_id.
    # if user is authenticated
    if current_user.is_authenticated:

        # Try to retrieve the cart item for the product.
        try:
            # If the item already exists in the cart, increase its quantity by 1.
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity += 1  # cart_item.quantity = cart_item.quantity +1
            cart_item.save()

        # If the item doesn't exist in the cart, create a new cart item with quantity 1.
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,

            )
            cart_item.save()

        # Redirect the user to the cart page.
        return redirect('cart')

     # if the user is not authenticated
    else:
        # Try to retrieve the cart associated with the user's session.
        try:

            # Get the cart using the cart_id stored in the session.
            # or this will get the cart using the cart id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:

            # If no cart exists, create a new one with a unique cart_id.
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        # Save the cart to the database.
        cart.save()

        # Try to retrieve the cart item for the product.
        try:
            # If the item already exists in the cart, increase its quantity by 1.
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1   #cart_item.quantity = cart_item.quantity +1
            cart_item.save()

        # If the item doesn't exist in the cart, create a new cart item with quantity 1.
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,

            )
            cart_item.save()

        # Redirect the user to the cart page.
        return redirect('cart')


# This function removes a product from the shopping cart one by one.
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


# This function removes all identical product from the shopping cart at once using the remove btn.
def remove_cart_item(request, product_id, cart_item_id,):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


# This function retrieves the cart items associated with the user's session and calculates the total price and quantity.
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # Try to retrieve the cart associated with the user's session.
            cart = Cart.objects.get(cart_id=_cart_id(request))

            # Retrieve all active cart items associated with the cart.
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # Iterate through each cart item to calculate the total price and quantity.
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Calculate total price.
            quantity += cart_item.quantity # Calculate total quantity.

    except ObjectDoesNotExist:
        pass  # Ignore if cart or cart items do not exist for the user's session.

    # Prepare the context dictionary with total price, total quantity, and cart items.
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }

    # Render the cart page with the calculated data.
    return render(request, 'products/cart.html', context )


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None, tax=0, grand_total=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # Try to retrieve the cart associated with the user's session.
            cart = Cart.objects.get(cart_id=_cart_id(request))

            # Retrieve all active cart items associated with the cart.
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # Iterate through each cart item to calculate the total price and quantity.
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Calculate total price.
            quantity += cart_item.quantity  # Calculate total quantity.
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # Ignore if cart or cart items do not exist for the user's session.

    # Prepare the context dictionary with total price, total quantity, and cart items.
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'products/checkout.html', context)