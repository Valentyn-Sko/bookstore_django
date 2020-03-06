import paypalrestsdk
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import *


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
    print("book_details")
    context = {
        'book': Book.objects.get(title__iexact=title),
    }
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
        else:
            return redirect('index')


def complete_order(request, processor):
    if request.user.id is not None:
        cart = Cart.objects.filter(user=request.user.id)
        print(list(cart))
        for c in cart:  # kostil
            cart1 = c  # kostil
        cart = cart1
        if processor == 'paypal':
            payment = paypalrestsdk.Payment.find(cart1.payment_id)
            if payment.execute({'payer_id': payment.payer.payer_info.payer_id}):
                message = "Success! Your order has been completed. Payment ID: %s" % (payment.id)
                cart.active = False
                cart.order_date = timezone.now()
                cart.save()
            else:
                message = "There was a problem with transaction. Error %s" % (payment.error.message)
            context = {
                'message': message,
            }
            return render(request, 'store/order_complete.html', context)
        else:
            return redirect('index')
