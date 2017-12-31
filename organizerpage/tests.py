from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from unittest.mock import Mock, patch
from test_me_app.models import *

import organizerpage.urls
import json

from unittest.mock import *


class TestRegister(TestCase):

    def test_register_success(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"group": "a",'
                                                '"email":"1@1.com",'
                                                '"verifyFileUrl":"/a/a"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

    def test_register_failed_by_invalid_email(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"group": "a",'
                                                '"email":"1@",'
                                                '"verifyFileUrl":"/a/a"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Email format error.')

    def test_register_failed_by_invalid_group_name(self):
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


class UserCenterTest(TestCase):

    def test_get_correct(self):
        found = resolve('/personal_info', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id": "1"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data'], "1")


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
