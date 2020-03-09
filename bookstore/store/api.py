from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from store.models import Book, Review


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        filds = ['username']
        authentication = SessionAuthentication()


class BookResource(ModelResource):
    class Meta:
        queryset = Book.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()


class ReviewResource(ModelResource):
    book = fields.ToOneField(BookResource, 'book')
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset = Review.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        filtering = {
            'book': ALL_WITH_RELATIONS,
        }
