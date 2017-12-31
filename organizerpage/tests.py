from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from test_me_app.models import *

import organizerpage.urls
import json

from unittest.mock import *


class TestRegister(TestCase):

    def test_post_register_successfully(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"group": "a",'
                                                '"email":"1@1.com",'
                                                '"verifyFileUrl":"/a/a"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

    def test_post_register_failed_by_invalid_email(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"group": "a",'
                                                '"email":"1@",'
                                                '"verifyFileUrl":"/a/a"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Email format error.')

    def test_post_register_failed_by_invalid_group_name(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"group": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                                                'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",'
                                                '"email":"1@1.com",'
                                                '"verifyFileUrl":"/a/a"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'The length of group name is restricted to 128.')


class TestUserCenter(TestCase):

    def setUp(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"group": "a",'
                                                '"email":"1@1.com",'
                                                '"verifyFileUrl":"/a/a"}')
        found.func(request)

    def test_post_change_info_successfully(self):
        found = resolve('/personal_info', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"nickname":"1", "avatarUrl":"1",'
                                                '"description": "a",'
                                                '"contactPhone": "13051330768",'
                                                '"email":"1@1.com"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

    def test_post_change_info_failed_by_invalid_nickname(self):
        found = resolve('/personal_info', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"nickname":"111111111111111111111", "avatarUrl":"1",'
                                                '"description": "a",'
                                                '"contactPhone": "13051330768",'
                                                '"email":"1@1.com"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'The length of nickname is restricted to 20.')


    def test_post_change_info_failed_by_invalid_phoneNum(self):
        found = resolve('/personal_info', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"nickname":"1", "avatarUrl":"1",'
                                                '"description": "a",'
                                                '"contactPhone": "130513307681",'
                                                '"email":"1@1.com"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Phone number invalid or not a cell phone number.')


    def test_post_change_info_failed_by_invalid_email(self):
        found = resolve('/personal_info', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"nickname":"1", "avatarUrl":"1",'
                                                '"description": "a",'
                                                '"contactPhone": "13051330768",'
                                                '"email":"1@com"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Email format error.')


class TestPlayerRegister(TestCase):

    def test_register_wrong_input(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        # wrong player type
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"email":"1@1.com", "group": "test_group",'
                                                '"gender":"male", "playerType":5, "birthday":"2017-11-23",'
                                                '"verifyFileUrl":""}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['msg'], 'Wrong organizer type')
        # wrong gender
        request.body.decode = Mock(return_value='{"username":"2", "password":"2",'
                                                '"email":"2@2.com", "group": "test_group",'
                                                '"gender":"unknown","playerType":0, "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['msg'], 'Wrong gender')

    def test_register_success(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"3", "password":"3",'
                                                '"email":"2@2.com", "group": "test_group",'
                                                '"gender":"female", "playerType":1, "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

# Create your tests here.
