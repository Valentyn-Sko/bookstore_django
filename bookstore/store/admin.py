from django.contrib import admin

from .models import Book, Genre, Author, Review, BookOrder, Cart


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'price', 'stock', 'get_genres',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'user', 'text', 'publish_date',)


class BookOrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'cart', 'quantity',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'order_date',)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(BookOrder, BookOrderAdmin)
admin.site.register(Cart, CartAdmin)

# user:valentyn
# pass:qwert
