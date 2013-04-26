from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^cookie-lang/?$', 'main.views.cookie_lang'),
    (r'^$', 'main.views.index'),
)