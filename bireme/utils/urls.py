from django.urls import path, re_path

from utils import views as utils_views

app_name = 'utils'

urlpatterns = [
    re_path(r'^$', utils_views.cookie_lang, name='cookie_lang'),
]
