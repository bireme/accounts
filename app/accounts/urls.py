"""
URL configuration for accounts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# enable django admin:
admin.autodiscover()

urlpatterns = [
    # Main app URLs at root
    path('', include('main.urls')),

    # Admin interface
    path('admin/', admin.site.urls),

    # Registration/authentication URLs
    path('accounts/', include('registration.urls')),

    # Internationalization and utils URLs
    path('i18n/', include('django.conf.urls.i18n')),
    path('cookie-lang/', include('utils.urls')),

    # TODO: Add these URL includes when the respective apps are migrated
    # path('api/', include('api.urls')),

]

# TODO: Add rosetta URLs when rosetta app is properly configured
# if 'rosetta' in settings.INSTALLED_APPS:
#     urlpatterns += [
#         re_path(r'^rosetta/', include('rosetta.urls'))
#     ]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
