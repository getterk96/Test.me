# -*- coding: utf-8 -*-
#
from django.conf.urls import url
from playerpage.views import *

urlpatterns = [
    url(r'^register$', PlayerRegister.as_view()),
    url(r'^personal_info$', PlayerPersonalInfo.as_view()),
    url(r'^participating_contests$', PlayerParticipatingContests.as_view()),
    url(r'^contest/detail$', PlayerContestDetail.as_view()),
    url(r'^period/detail$', PlayerPeriodDetail.as_view()),
    url(r'^question/detail$', PlayerQuestionDetail.as_view()),
    url(r'^question/submit$', PlayerQuestionSubmit.as_view()),
    url(r'^team/list$', PlayerTeamList.as_view()),
    url(r'^team/detail$', PlayerTeamDetail.as_view()),
]
