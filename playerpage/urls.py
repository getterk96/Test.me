# -*- coding: utf-8 -*-
#
from django.conf.urls import url
from playerpage.views import *

urlpatterns = [
    url(r'^register$', PlayerRegister.as_view()),
    url(r'^personal_info$', PlayerPersonalInfo.as_view()),
    url(r'^participating_contests$', PlayerParticipatingContests.as_view()),
    url(r'^contest/detail$', PlayerContestDetail.as_view()),
    url(r'^contest/search/simple$', PlayerContestSearchSimple.as_view()),
    url(r'^period/detail$', PlayerPeriodDetail.as_view()),
    url(r'^question/detail$', PlayerQuestionDetail.as_view()),
    url(r'^question/submit$', PlayerQuestionSubmit.as_view()),
    url(r'^team/list$', PlayerTeamList.as_view()),
    url(r'^team/create$', PlayerTeamCreate.as_view()),
    url(r'^team/detail$', PlayerTeamDetail.as_view()),
    url(r'^team/dismiss$', PlayerTeamDismiss.as_view()),
    url(r'^team/invitation$', PlayerTeamInvitation.as_view()),
    url(r'^team/signup$', PlayerTeamSignUp.as_view()),
    url(r'^appeal/create$', PlayerAppealCreate.as_view()),
    url(r'^appeal/detail$', PlayerAppealDetail.as_view()),
    url(r'^appeal/remove$', PlayerAppealRemove.as_view()),
    url(r'^player/search$', PlayerSearch.as_view())
]
