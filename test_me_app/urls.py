from django.conf.urls import url
from test_me_app.views import *

urlpatterns = [
    url(r'^index', Index.as_view()),
    url(r'^login', Login.as_view()),
]
