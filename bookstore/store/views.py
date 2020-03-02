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
        cart = Cart.objects.get(user=request.user.id, active=True)
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
