from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from unittest.mock import Mock, patch
import playerpage.urls
import json

# Create your tests here.


class TestRegister(TestCase):

    def test_register_wrong_type(self):
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"email":"1@1.com", "gender":"male",'
                                                '"playerType":"小学生", "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Signup fail')

    def test_register_success(self):
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"2", "password":"2",'
                                                '"email":"2@2.com", "gender":"male",'
                                                '"playerType":"研究生", "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)