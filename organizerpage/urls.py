# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from organizerpage.views import *

urlpatterns = [
    url(r'^contest/detail/?$', ContestDetail.as_view()),
    url(r'^contest/createslots/?$', ContestCreateSlots.as_view()),
    url(r'^contest/createbasic/?$', ContestCreateBasic.as_view()),
    url(r'^contest/upload/?$', ContestUpload.as_view()),
]
