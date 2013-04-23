from django.conf.urls import patterns, url, include
from api import UserResource

user_resource = UserResource()

urlpatterns = patterns('',

    url(r'^auth/', include(user_resource.urls)),
    
)