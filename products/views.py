from django.shortcuts import render, get_object_or_404
from .models import Product
from cart.models import CartItem, Cart
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    # Calculate the cart quantity
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        quantity = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        quantity = 0  # If cart doesn't exist, set quantity to 0

    context = {
        'Products': Product.objects.all(),
        'quantity': quantity,
    }
    return render(request, 'products/home.html', context)


def products(request):
    # Calculate the cart quantity
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        quantity = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        quantity = 0  # If cart doesn't exist, set quantity to 0


    # Pagination
    all_products = Product.objects.all().order_by('id')
    paginator = Paginator(all_products, 3)  # Change 4 to the number of products per page you desire

    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,  # Use the paginated products here, not the Product class
        'quantity': quantity,
    }
    return render(request, 'products/products.html', context)


def about(request):
    # Calculate the cart quantity
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        quantity = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        quantity = 0  # If cart doesn't exist, set quantity to 0

    context = {
        'quantity': quantity,
    }

    return render(request, 'products/about.html', context)


def details(request, product_id):  #This line defines a function named details that takes two parameters: request, which is a Django HTTP request object, and product_id, which represents the ID of the product being requested.

    # Calculate the cart quantity
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        quantity = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        quantity = 0  # If cart doesn't exist, set quantity to 0


    # This line starts a try block, which allows you to catch exceptions that may occur during the execution of the code within the block.
    try:
        single_product = get_object_or_404(Product, pk=product_id)    #get_object_or_404(Product, pk=product_id): This line attempts to retrieve a single Product object from the database based on the provided product_id. get_object_or_404 is a Django shortcut that either returns the object if it exists or raises a 404 Not Found error if it doesn't. single_product: If the get_object_or_404 call is successful, the retrieved Product object is assigned to the variable single_product.
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'quantity': quantity,
        'in_cart': in_cart,
    }
    return render(request, 'products/details.html', context)


# this define the serach function
def search(request):
    products = None  # Initialize products variable to None

    # Calculate the cart quantity
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        quantity = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        quantity = 0  # If cart doesn't exist, set quantity to 0

    # Check if 'keyword' parameter is present in the request's GET parameters
    if 'keyword' in request.GET:
        # If 'keyword' is present, retrieve its value
        keyword = request.GET['keyword']

        # Check if 'keyword' has a non-empty value
        if keyword:
            # Perform a query on the Product model to filter records based on keyword
            # Use case-insensitive search on both 'description' and 'name' fields
            # Order the results by the 'created_date' field in descending order
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(name__icontains=keyword)
            )

    # Prepare the context dictionary to pass data to the template
    context = {
        'products': products,  # Use lowercase 'products' here
        'quantity': quantity,
    }

    # Render the 'products/products.html' template with the context data
    return render(request, 'products/products.html', context)