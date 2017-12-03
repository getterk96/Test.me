# -*- coding: utf-8 -*-
#
from django.conf.urls import url
from adminpage.views import *

urlpatterns = [
    url(r'^appeal/detail$', AppealDetail.as_view()),
    url(r'^appeal/remove$', AppealRemove.as_view()),
]
