from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Book


def index(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)

        uname = query[0].username
        return render(request, 'template.html', {"uname": uname})

    return render(request, 'template.html')


def store(request):
    count = Book.objects.all().count()

    return render(request, 'stock.html', context={'count': count})


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
