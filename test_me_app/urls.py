from django.conf.urls import url
from test_me_app.views import *

urlpatterns = [
    url(r'^index', Index.as_view()),
    url(r'^login', UserLogin.as_view()),
    url(r'^logout', UserLogout.as_view()),
    url(r'^signup/player', PlayerSignup.as_view()),
    url(r'^signup/organizer', OrganizerSignup.as_view()),
    url(r'^uploadfile', UploadFile.as_view()),
    url(r'^center', UserCenter.as_view())
]
