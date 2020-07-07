from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# enable django admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^', include('main.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.urls')),
    path('api/', include('api.urls')),

    # internationalization
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^cookie-lang/', include('utils.urls')),
]


# messages translation
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
