from django.conf.urls import url
from test_me_app.views import *

urlpatterns = [
    url(r'^login', Login.as_view()),
    url(r'^logout', Logout.as_view()),
    url(r'^upload', Upload.as_view()),
    url(r'^user_type', UserType.as_view()),
    url(r'^change_password', ChangePassword.as_view()),
    url(r'^user_id', UserId.as_view()),
    url(r'^forum/list', ForumList.as_view()),
    url(r'^forum/post/create', ForumPostCreate.as_view()),
    url(r'^forum/detail', ForumDetail.as_view()),
    url(r'^forum/reply/create', ForumReplyCreate.as_view())
]
