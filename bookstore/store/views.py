from django.shortcuts import render

from store.models import Book


def index(request):
    return render(request, 'template.html')


def store(request):
    count = Book.objects.all().count()
    return render(request, 'stock.html', context={'count': count})
