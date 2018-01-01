from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from test_me_app.models import *

import organizerpage.urls
import playerpage.urls
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
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"2", "password":"1",'
                                                '"group": "a",'
                                                '"email":"2@1.com",'
                                                '"gender":"male",'
                                                '"playerType":0,'
                                                '"birthday":"2017-12-31"}')
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

    def test_get_info_successfully(self):
        found = resolve('/personal_info', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data']['email'], '1@1.com')

    def test_get_info_failed_by_not_a_organizer(self):
        found = resolve('/personal_info', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='')
        request.user = User.objects.get(username='2')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Organizer required')


class TestContestCreate(TestCase):

    def setUp(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"group": "a",'
                                                '"email":"1@1.com",'
                                                '"verifyFileUrl":"/a/a"}')
        found.func(request)

    def test_post_create_contest_successfully(self):
        found = resolve('/contest/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"test",'
                                                '"description":"test",'
                                                '"logoUrl": "None",'
                                                '"bannerUrl":"None",'
                                                '"signUpStart":"2017-12-31T04:00:54.528Z",'
                                                '"signUpEnd": "2017-12-31T04:00:55.528Z",'
                                                '"availableSlots": 0,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


    def test_post_create_contest_failed_by_name_too_long (self):
        found = resolve('/contest/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"testtesttesttesttesttesttesttest'
                                                'testtesttesttesttesttesttesttestt",'
                                                '"description":"test",'
                                                '"logoUrl": "None",'
                                                '"bannerUrl":"None",'
                                                '"signUpStart":"2017-12-31T04:00:54.528Z",'
                                                '"signUpEnd": "2017-12-31T04:00:55.528Z",'
                                                '"availableSlots": 0,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], "The length of name is restricted to 64.")

    def test_post_create_contest_failed_by_url_too_long (self):
        found = resolve('/contest/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"test",'
                                                '"description":"test",'
                                                '"logoUrl": "NoneNoneNoneNoneNoneNoneNoneNone'
                                                'NoneNoneNoneNoneNoneNoneNoneNone'
                                                'NoneNoneNoneNoneNoneNoneNoneNone'
                                                'NoneNoneNoneNoneNoneNoneNoneNone'
                                                'NoneNoneNoneNoneNoneNoneNoneNone'
                                                'NoneNoneNoneNoneNoneNoneNoneNone'
                                                'NoneNoneNoneNoneNoneNoneNoneNone'
                                                'NoneNoneNoneNoneNoneNoneNoneNoneNone",'
                                                '"bannerUrl":"None",'
                                                '"signUpStart":"2017-12-31T04:00:54.528Z",'
                                                '"signUpEnd": "2017-12-31T04:00:55.528Z",'
                                                '"availableSlots": 0,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], "The length of url is restricted to 256.")


class TestContests(TestCase):

    def setUp(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"1", "password":"1",'
                                                '"group": "a",'
                                                '"email":"1@1.com",'
                                                '"verifyFileUrl":"/a/a"}')
        found.func(request)
        found = resolve('/contest/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"test",'
                                                '"description":"test",'
                                                '"logoUrl": "None",'
                                                '"bannerUrl":"None",'
                                                '"signUpStart":"2017-12-31 05:05:05",'
                                                '"signUpEnd": "2017-12-31 05:05:06",'
                                                '"availableSlots": 0,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        result = found.func(request)
        result = result

# Create your tests here.
