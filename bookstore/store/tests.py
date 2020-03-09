from decimal import Decimal

from django.test import TestCase

# Create your tests here.

from .models import Author, Book, Cart
from django.urls import reverse
from django.contrib.auth.models import User as U


class StoreViewTestCase(TestCase):
    def setUp(self):
        self.user = U.objects.create_user(
            username='james',
            email='some@email.com',
            password='bla123'
        )
        author = Author.objects.create(first_name='Stephen', last_name='King')
        book = Book.objects.create(title='It',author=author,description='Some Dest', price=10.11, stock=5)

    def test_index(self):
        resp = self.client.get('/store/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('books' in resp.context)
        self.assertTrue(resp.context['books'].count() > 0)

    def test_cart(self):
        resp = self.client.get('/store/cart/')
        self.assertEqual(resp.status_code, 302)

    def test_book_detail(self):
        resp = self.client.get('/store/book/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['book'].pk,1)
        self.assertEqual(resp.context['book'].title, 'It')
        resp = self.client.get('/store/book/2')
        self.assertEqual(resp.status_code, 404)

    def test_add_to_cart(self):
        self.logged_in = self.client.login(username='james', password='bla123')
        self.assertTrue(self.logged_in)
        resp = self.client.get('/store/add/1/')
        resp = self.client.get('/store/cart/')
        #print(resp)
        #self.assertEqual(resp.context, 1)
        #self.assertEqual(resp.context['total'], Decimal('10.11'))
        #self.assertEqual(resp.context['cart'].count(), 1)
        #self.assertEqual(resp.context['cart'].get().quantity, 1)
