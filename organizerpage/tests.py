from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

import organizerpage.urls, json

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


class UserCenterTest(TestCase):

    def test_get_correct(self):
        found = resolve('/personal_info', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id": "1"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data'], "1")

# Create your tests here.
