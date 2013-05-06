from django.conf.urls import patterns, url, include
from api import UserResource

user_resource = UserResource()

urlpatterns = patterns('',

    url(r'^auth/', include(user_resource.urls)),

    url(r'^get_ccs/?$', 'api.views.get_ccs')
    
)