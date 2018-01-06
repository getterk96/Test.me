from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from unittest.mock import Mock, patch
from django.contrib import auth
from test_me_app.models import User_profile
import test_me_app.urls
import json


# Create your tests here.

class TestLogin(TestCase):

    def test_login_get_not_login(self):
        found = resolve('/login', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=Mock(is_authenticated=False))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 3)
        self.assertEqual(response['msg'], 'Not login')

    def test_login_get_login(self):
        found = resolve('/login', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=Mock(is_authenticated=True))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

    def test_login_post_no_params(self):
        found = resolve('/login', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)

    def test_login_post_no_enough_params(self):
        found = resolve('/login', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)

    def test_login_post_wrong_username_or_password(self):
        found = resolve('/login', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1"}')
        with patch.object(auth, 'authenticate', return_value=False):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['code'], 3)
            self.assertEqual(response['msg'], 'Wrong username or password')

    def test_login_post_success(self):
        found = resolve('/login', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1"}')
        with patch.object(auth, 'authenticate', return_value=True):
            with patch.object(auth, 'login', return_value=True):
                response = json.loads(found.func(request).content.decode())
                self.assertEqual(response['code'], 0)


class TestLogout(TestCase):

    def test_logout(self):
        found = resolve('/logout', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=Mock(is_authenticated=True))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        with patch.object(auth, 'logout', side_effect=Exception):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['code'], 2)
            self.assertEqual(response['msg'], 'Logout fail')

    def test_logout_post_success(self):
        found = resolve('/logout', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=Mock(is_authenticated=True))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        with patch.object(auth, 'logout', return_value=True):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['code'], 0)


class TestUpload(TestCase):

    def test_upload_fail(self):
        found = resolve('/upload', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"file":[], "destination":"test_destination"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Upload failed')


class TestUserType(TestCase):

    def test_user_type_get(self):
        found = resolve('/user_type', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='GET',
                       user=Mock(is_authenticated=True,
                                 user_profile=Mock(user_type=User_profile.PLAYER,
                                                   status=User_profile.NORMAL)))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'], User_profile.PLAYER)
