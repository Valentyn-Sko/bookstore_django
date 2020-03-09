import form as form
import paypalrestsdk
import stripe
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geoip2 import GeoIP2
from django.template import Context
from django.template.loader import render_to_string

from bookstore import settings
from .models import *
from .forms import ReviewForm


def index(request):
    books = Book.objects.all()
    print(books)
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)

        uname = query[0].username
        return render(request, 'template.html', context={"uname": uname, "books": books})

    return render(request, 'template.html', context={"books": books})


def store(request):
    count = Book.objects.all().count()

    return render(request, 'stock.html', context={'count': count})


def book_details(request, title):
    book = Book.objects.get(title__iexact=title)  # Book.obgects.get(pk=book_id)
    context = {
        'book': book
    }
    if request.user.id is not None:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_review = Review.objects.create(
                    user=request.user,
                    book=context['book'],
                    text=form.cleaned_data.get('text')
                )
                new_review.save()
        else:
            if Review.objects.filter(user=request.user, book=context['book']).count() == 0:
                form = ReviewForm()
                context['form'] = form
    context['reviews'] = book.review_set.all()
    ip_s = request.META.get('REMOTE_ADDR')
    geo_info = ''
    if ip_s != '127.0.0.1':
        geo_info = GeoIP2().city(ip_s)
    if not geo_info:
        geo_info = GeoIP2().city('93.178.204.228')
    context['geo_info'] = geo_info
    print(geo_info)

    return render(request, 'store/detail.html', context=context)


# def loginpage(request):      # for custom loinpage (../signin/)
#    if request.method == 'POST':
#        username = request.POST['username']
#        password = request.POST['password']
#        post = User.objects.filter(username=username)
#        if post:
#            username = request.POST['username']
#            request.session['username'] = username
#            return redirect("profile")
#        else:
#            return render(request, 'store/login.html', {})
#    return render(request, 'store/login.html', {})


def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'profile.html', {"query": query})
    else:
        return render(request, 'registration/login.html', {})


# def logout(request):  #for custom logout
#    try:
#        del request.session['username']
#    except:
#        pass
#    #return loginpage(request)
#    return render(request, 'store/logout.html', {})


def add_to_cart(request, id):
    if request.user.id is not None:
        try:
            book = Book.objects.get(pk=id)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                cart = Cart.objects.get(user=request.user.id, active=True)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(
                    user=request.user
                )
                cart.save()
            cart.add_to_cart(id)
        return redirect('cart')
    else:
        return redirect('index')


def remove_from_cart(request, id):
    if request.user.id is not None:
        try:
            book = Book.objects.get(pk=id)
        except ObjectDoesNotExist:
            pass
        else:
            cart = Cart.objects.get(user=request.user, active=True)
            cart.remove_from_cart(id)
        return redirect('cart')
    else:
        return redirect('index')


def cart(request):
    if request.user.id is not None:
        try:
            cart = Cart.objects.get(user=request.user.id, active=True)
        except ObjectDoesNotExist:
            return render(request, 'store/cart.html', context={})
        orders = BookOrder.objects.filter(cart=cart)
        total = 0
        count = 0

        for order in orders:
            total += (order.book.price * order.quantity)
            count += order.quantity
        context = {
            'cart': orders,
            'total': total,
            'count': count,
            'key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, 'store/cart.html', context)
    else:
        return redirect('index')


def checkout(request, processor):
    if request.user.id is not None:
        cart = Cart.objects.filter(user=request.user.id, active=True)
        orders = BookOrder.objects.filter(cart__in=cart)
        if processor == 'paypal':
            redirect_url = checkout_paypal(request, cart, orders)
            return redirect(redirect_url)
        elif processor == 'stripe':
            token = request.POST('stripeToken')
            status = checkout_strip(cart, orders, token)
            if status:
                return redirect(reverse('process_order', args=['stripe']))
            else:
                return redirect('order_error', context={'message': 'There was a problem processing your payment.'})
    else:
        return redirect('index')


def checkout_paypal(request, cart, orders):
    if request.user.id is not None:
        items = []
        total = 0
        for order in orders:
            total += (order.book.price * order.quantity)
            book = order.book
            item = {
                'name': book.title,
                'sku': book.id,
                'currency': 'USD',
                'quantity': order.quantity,
                'price': str(book.price),
            }
            items.append(item)
        print(items)
        paypalrestsdk.configure({
            'mode': 'sandbox',
            'client_id': 'AbFIBGQdDCUSGQwZJrYqVfPeRwDbVVyCPeyJcEmM1BrWx5OmTzweOsa_ReeYSsHD2yFcFWyFlp3j80xf',
            'client_secret': 'EBGZF59t3ItHsjykiTW2MrIWH07SRkKwmy3OaTMhB0zdxqGSLE4SfUtKAqbN1vvydhDu9SIs5W-WkFCh',
        })
        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {
                'payment_method': 'paypal'
            },
            'redirect_urls': {
                'return_url': 'http://localhost:5000/store/process/paypal',
                'cancel_url': 'http://localhost:5000/store'
            },
            'transactions': [{
                'item_list': {'items': items},
                'amount': {
                    'total': str(total),
                    'currency': 'USD'
                },
                'description': 'Book order.'
            }]

        })

        if payment.create():
            cart_instance = cart.get()
            cart_instance.payment_id = payment.id
            cart_instance.save()
            for link in payment.links:
                if link.method == 'REDIRECT':
                    redirect_url = str(link.href)
                    return redirect_url
        else:
            print(payment.error)
            return reverse('order_error')
    else:
        return redirect('index')


def checkout_strip(cart, orders, token):
    stripe.api_key = 'sk_test_oetchDORscwl8d4I4u1ve5rI00AxIIxzpn'
    total = 0
    for order in orders:
        total += (order.quantity * order.book.price)
    status = True
    try:
        charge = stripe.Charge.create(
            amount=int(total * 100),
            currency='USD',
            source=token,
            metadata={'order_id': cart.get().id}
        )
        cart_instanse = cart.get()
        cart_instanse.payment_id = charge.id
        cart_instanse.save()
    except stripe.error.CardError as e:
        status = False
    return status


def order_error(request):
    if request.user.id is not None:
        return render(request, 'store/order_error.html')
    else:
        return redirect('index')


def process_order(request, processor):
    if request.user.id is not None:
        if processor == 'paypal':
            payment_id = request.GET.get('paymentId')
            cart = Cart.objects.filter(payment_id=payment_id)
            orders = BookOrder.objects.filter(cart__in=cart)
            total = 0
            for order in orders:
                total += (order.book.price * order.quantity)
            context = {
                'cart': orders,
                'total': total,
            }
            return render(request, 'store/process_order.html', context)
        elif processor == 'stripe':
            return JsonResponse({'redirect_url': reverse('complete_order', args=['stripe'])})
    else:
        return redirect('index')


def complete_order(request, processor):
    if request.user.id is not None:
        cart = Cart.objects.filter(user=request.user.id)
        for c in cart:  # kostil
            cart1 = c  # kostil
        cart = cart1
        if processor == 'paypal':
            payment = paypalrestsdk.Payment.find(cart1.payment_id)
            if payment.execute({'payer_id': payment.payer.payer_info.payer_id}):
                message = "Success! Your order has been completed. Payment ID: %s" % (payment.id)
                cart.active = False
                cart.order_date = timezone.now()
                cart.payment_type = 'Paypal'
                cart.save()
                qty_update(cart)
            else:
                message = "There was a problem with transaction. Error %s" % (payment.error.message)
            context = {
                'message': message,
            }
            return render(request, 'store/order_complete.html', context)
        elif processor == 'stripe':
            cart.active = False
            cart.order_date = timezone.now()
            cart.payment_type = 'Stripe'
            cart.save()
            qty_update(cart)
            message = "Success! Your order has been completed. Payment ID: %s" % (cart.payment_id)
            context = {
                'message': message,
            }
            return render(request, 'store/order_complete.html', context)

    else:
        return redirect('index')


def qty_update(cart):
    orders = BookOrder.objects.filter(cart=cart)
    total = 0
    for order in orders:
        book = Book.objects.get(id=order.book.id)
        book.stock -= order.quantity
        book.save()

        # thanks email
        rom_email = 'some@gmail.com'
        to_email = ('i0000017vs@gmail.com',)

        email_context = Context({
            'username': cart.user,
            'orders': orders
        })

        subject = 'hello'
        text_content = 'This is an important message.'
        html_content = '<p>This is an <strong>important</strong> message.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
