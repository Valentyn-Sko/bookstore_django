from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.store, name='store'),
    path('accounts/profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    # path('signin/', views.loginpage, name='loginpage'),
    path('profile/', views.profile, name='profile'),
    # path('accounts/', include('django_registration.backends.activation.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('book/<title>', views.book_details, name='book_details'),
    # path('logout/', views.logout, name='logout'),
    path('add/<id>', views.add_to_cart, name='add_to_cart'),
    path('remove/<id>', views.remove_from_cart, name='remove_from_cart'),
    path('book/<title>', views.book_details, name='book_details'),
    path('checkout/<processor>', views.checkout, name='checkout'),
    path('process/<processor>', views.process_order, name='process_order'),
    path('order_error', views.order_error, name='order_error'),
    path('complete_order/<processor>', views.complete_order, name='complete_order'),

]
