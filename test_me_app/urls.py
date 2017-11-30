from django.conf.urls import url
from test_me_app.views import *

urlpatterns = [
    url(r'^login', Login.as_view()),
    url(r'^logout', Logout.as_view()),
    url(r'^upload', Upload.as_view()),
    url(r'^user_type', UserType.as_view(),)
]
