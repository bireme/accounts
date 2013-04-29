from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^cookie-lang/?$', 'utils.views.cookie_lang'),
)
