from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from store.models import Book


def index(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)

        uname=query[0].username
        return render(request, 'store/template.html', {"uname": uname})

    return render(request, 'store/template.html')


def store(request):
    count = Book.objects.all().count()
    login_logout=False
    if request.session.has_key('username'):
        login_logout=True
    return render(request, 'store/stock.html', context={'count': count, 'login_logout': login_logout})


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        post = User.objects.filter(username=username)
        if post:
            username = request.POST['username']
            request.session['username'] = username
            return redirect("profile")
        else:
            return render(request, 'store/login.html', {})
    return render(request, 'store/login.html', {})


def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'store/profile.html', {"query": query})
    else:
        return render(request, 'store/login.html', {})


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    #return loginpage(request)
    return render(request, 'store/logout.html', {})
