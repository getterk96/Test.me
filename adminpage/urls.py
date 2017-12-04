# -*- coding: utf-8 -*-
#
from django.conf.urls import url
from adminpage.views import *

urlpatterns = [
    url(r'^user/list$', AdminUserList.as_view()),
    url(r'^user/search$', AdminUserSearch.as_view()),
    url(r'^appeal/detail$', AdminAppealDetail.as_view()),
    url(r'^appeal/remove$', AdminAppealRemove.as_view()),
]
