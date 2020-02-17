from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('stock/', store, name='store'),
    #path('accounts/', include('django_registration.backends.activation.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
#django_registration.backends.one_step.urls'
    #django_registration.backends.activation.urls'
]
