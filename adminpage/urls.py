# -*- coding: utf-8 -*-
#
from django.conf.urls import url
from adminpage.views import *

urlpatterns = [
    url(r'^user/list$', AdminUserList.as_view()),
    url(r'^user/search$', AdminUserSearch.as_view()),
    url(r'^user/delete$', AdminUserDelete.as_view()),
    url(r'^user/recover$', AdminUserRecover.as_view()),
    url(r'^player/detail$', AdminPlayerDetail.as_view()),
    url(r'^organizer/detail$', AdminOrganizerDetail.as_view()),
    url(r'^organizer/verification$', AdminOrganizerVerification.as_view()),
    url(r'^contest/list$', AdminContestList.as_view()),
    url(r'^contest/search$', AdminContestSearch.as_view()),
    url(r'^appeal/detail$', AdminAppealDetail.as_view()),
    url(r'^appeal/remove$', AdminAppealRemove.as_view()),
]
