# -*- coding: utf-8 -*-
#
from django.conf.urls import url
from playerpage.views import *

urlpatterns = [
    url(r'^register$', PlayerRegister.as_view()),
]
