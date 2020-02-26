from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.store, name='store'),
    path('accounts/profile/', views.profile, name='profile'),

    # path('signin/', views.loginpage, name='loginpage'),
    path('profile/', views.profile, name='profile'),
    # path('accounts/', include('django_registration.backends.activation.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('book/<title>', views.book_details, name='book_details'),
    # path('logout/', views.logout, name='logout'),
]
