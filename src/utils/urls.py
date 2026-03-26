from django.urls import path

from utils import views as utils_views

app_name = 'utils'

urlpatterns = [
    path('', utils_views.cookie_lang, name='cookie_lang'),
]