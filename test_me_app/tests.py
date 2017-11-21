from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from unittest.mock import Mock, patch
from django.contrib import auth
from test_me import settings
import test_me_app.urls
import json
import time


# Create your tests here.

def patcher_start(patchers):
    for patcher in patchers:
        patcher.start()


def patcher_stop(patchers):
    for patcher in patchers:
        patcher.stop()


class LoginTest(TestCase):

    def test_login_get(self):
        found = resolve('/login', urlconf=test_me_app.urls)
        # not login
        request = Mock(wraps=HttpRequest(), method='GET', user=Mock(is_authenticated=False))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 3)
        self.assertEqual(response['msg'], 'Not login')
        # already login
        request = Mock(wraps=HttpRequest(), method='GET', user=Mock(is_authenticated=True))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

    def test_login_post(self):
        found = resolve('/login', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        # no params
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)
        # no enough params
        request.body.decode = Mock(return_value='{"username":"1"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)
        # wrong username or password
        request.body.decode = Mock(return_value='{"username":"1", "password":"1"}')
        with patch.object(auth, 'authenticate', return_value=False):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['code'], 3)
            self.assertEqual(response['msg'], 'Wrong username or password')
        # login success
        with patch.object(auth, 'authenticate', return_value=True):
            with patch.object(auth, 'login', return_value=True):
                response = json.loads(found.func(request).content.decode())
                self.assertEqual(response['code'], 0)


class Logout(TestCase):

    def test_logout(self):
        found = resolve('/logout', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=Mock(is_authenticated=True))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        with patch.object(auth, 'logout', side_effect=Exception):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['code'], 2)
            self.assertEqual(response['msg'], 'Logout fail')
        with patch.object(auth, 'logout', return_value=True):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['code'], 0)


class UploadTest(TestCase):

    def test_upload_url(self):
        found=resolve('/upload', urlconf=test_me_app.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=Mock(is_authenticated=True))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"file":[{"name":"test_file.txt"}],"destination":"test_destination"}')
        with patch.object(time, 'strftime', return_value='20170101122333'):
            response = json.loads(found.func(request).content.decode())
            self.assertRaises(FileNotFoundError, msg="No such file or directory:" + settings.MEDIA_URL +
                " 'test_destination/20170101122333.txt'")