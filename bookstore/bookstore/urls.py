"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from tastypie.api import Api
from store.api import ReviewResource

v1_api = Api(api_name='v1')
v1_api.register(ReviewResource())


from bookstore import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls'), name='store'),
    path('accounts/profile/', RedirectView.as_view(url='/store')),
    #path('', include('social.apps.django_app.urls', namespace='social')),
    #path('accounts/', include('django_registration.backends.activation.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    path('api/', include(v1_api.urls)),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
