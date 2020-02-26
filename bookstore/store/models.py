from time import time

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, blank=True, unique=True)

    def __str__(self):
        return '{}'.format(self.first_name + ' ' + self.last_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.first_name + self.last_name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['last_name']


class Genre(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']


class Book(models.Model):
    title = models.CharField(max_length=200)
    # author = models.CharField(max_length=200)
    description = models.TextField(default="")
    publish_date = models.DateField(default=timezone.now())
    price = models.DecimalField(decimal_places=2, max_digits=8)
    stock = models.IntegerField(default=0)

    genres = models.ManyToManyField('Genre', blank=True, related_name='books')
    authors = models.ManyToManyField('Author', blank=True, related_name='books')

    def get_genres(self):
        return "\n".join([g.title for g in self.genres.all()])

    def get_authors(self):
        return "\n".join([g.first_name + ' ' + g.last_name for g in self.authors.all()])


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="")
    publish_date = models.DateField(default=timezone.now())
