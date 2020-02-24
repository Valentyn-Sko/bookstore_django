from django.contrib import admin

from .models import Book, Genre, Author


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'price', 'stock', 'get_genres',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)

#user:valentyn
#pass:qwert123