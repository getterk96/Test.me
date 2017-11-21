from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from unittest.mock import Mock, patch
import playerpage.urls
import json

# Create your tests here.


class TestRegister(TestCase):

    def test_register_wrong_input(self):
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        # wrong player type
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"email":"1@1.com", "group": "test_group",'
                                                '"gender":"male", "playerType":5, "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['msg'], 'Wrong player type')
        # wrong gender
        request.body.decode = Mock(return_value='{"username":"2", "password":"2",'
                                                '"email":"2@2.com", "group": "test_group",'
                                                '"gender":"unknown","playerType":0, "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['msg'], 'Wrong gender')

    def test_register_success(self):
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"3", "password":"3",'
                                                '"email":"2@2.com", "group": "test_group",'
                                                '"gender":"male", "playerType":1, "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)