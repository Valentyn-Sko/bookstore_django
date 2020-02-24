from django.contrib import admin

from .models import Book, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'get_genres')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)


#user:valentyn
#pass:qwert123