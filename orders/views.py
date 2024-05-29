from django.shortcuts import render, redirect
from cart.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        pk = request.session['order_id']
        order = Order.objects.get(pk=pk)
        order.is_verified = True
        order.save()
        context = {
            'placed_order': pk,
            'payment': payment,
        }
        return render(request, 'orders/success.html', context)

    else:
        messages.warning(request, 'Sorry, your order was not processed. Please contact our support.')
        return redirect('/')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('home')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all billing info inside the order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            payment = Payment.objects.create(amount=grand_total, email=current_user.email, user=current_user)
            payment.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # e.g., 20240305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            try:
                # Retrieve the order to ensure it exists
                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
                # Set order_id in the session
                request.session['order_id'] = order.id  # This line sets the order_id in the session

                pk = settings.PAYSTACK_PUBLIC_KEY
                context = {
                    'order': order,
                    'cart_items': cart_items,
                    'total': total,
                    'tax': tax,
                    'grand_total': grand_total,
                    'payment': payment,
                    'paystack_pub_key': pk,
                    'amount_value': payment.amount_value()
                }
                return render(request, 'orders/payment.html', context)
            except ObjectDoesNotExist:
                # Handle the case where the order does not exist
                return redirect('checkout')
        else:
            return redirect('checkout')