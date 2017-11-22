# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from organizerpage.views import *

urlpatterns = [
    url(r'^register?$', Register.as_view()),
    url(r'^personal_info?$', PersonalInfo.as_view()),
    url(r'^contest/organizing_contests?$', OrganizingContests.as_view()),
    url(r'^contest/batch_remove?$', ContestBatchRemove.as_view()),
    url(r'^contest/detail?$', ContestDetail.as_view()),
    url(r'^contest/createbasic?$', ContestCreateBasic.as_view()),
]
