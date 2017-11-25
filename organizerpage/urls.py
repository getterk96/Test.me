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
    url(r'^contest/create?$', ContestCreate.as_view()),
    url(r'^contest/remove?$', ContestRemove.as_view()),
    url(r'^contest/team?$', ContestTeam.as_view()),
    url(r'^contest/team_batch_manage?$', ContestTeamBatchManage.as_view()),
    url(r'^period/create?$', PeriodCreate.as_view()),
    url(r'^period/detail?$', PeriodCreate.as_view()),
    url(r'^period/remove?$', PeriodCreate.as_view()),
    url(r'^question/create?$', PeriodCreate.as_view()),
    url(r'^question/detail?$', PeriodCreate.as_view()),
    url(r'^question/remove?$', PeriodCreate.as_view()),

]
