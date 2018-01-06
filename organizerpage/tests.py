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
                                                '"email":"1@1.com",'
                                                '"group":0}')
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
                                                '"email":"1@1.com",'
                                                '"group":0}')
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
                                                '"email":"1@1.com",'
                                                '"group":0}')
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
                                                '"email":"1@.com",'
                                                '"group":0}')
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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 0,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

    def test_post_create_contest_failed_by_name_too_long(self):
        found = resolve('/contest/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"testtesttesttesttesttesttesttest'
                                                'testtesttesttesttesttesttesttestt",'
                                                '"description":"test",'
                                                '"logoUrl": "None",'
                                                '"bannerUrl":"None",'
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 0,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], "The length of name is restricted to 64.")

    def test_post_create_contest_failed_by_url_too_long(self):
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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 0,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        found.func(request)

    def test_get_organizing_contest_successfully(self):
        found = resolve('/contest/organizing_contests', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data'][0]['name'], 'test')

    def test_get_contest_detail_successfully(self):
        found = resolve('/contest/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + '}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data']['name'], 'test')

    def test_get_contest_detail_failed_by_contest_not_exist(self):
        found = resolve('/contest/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id":10086}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'No Such Contest')

    def test_post_contest_detail_successfully(self):
        found = resolve('/contest/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"name":"test0",'
                                                                    '"description":"test",'
                                                                    '"logoUrl": "None",'
                                                                    '"bannerUrl":"None",'
                                                                    '"signUpStart":"2017-12-31 04:00:54",'
                                                                    '"signUpEnd": "2017-12-31 04:00:55",'
                                                                    '"availableSlots": 0,'
                                                                    '"maxTeamMembers": 5,'
                                                                    '"signUpAttachmentUrl": "None",'
                                                                    '"level": 0,'
                                                                    '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(Contest.objects.get(id=int(str_id)).name, 'test0')

    def test_post_contest_detail_failed_by_end_earlier_than_start(self):
        found = resolve('/contest/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"name":"test",'
                                                                    '"description":"test",'
                                                                    '"logoUrl": "None",'
                                                                    '"bannerUrl":"None",'
                                                                    '"signUpStart":"2017-12-31 04:00:54",'
                                                                    '"signUpEnd": "2017-12-31 04:00:53",'
                                                                    '"availableSlots": 0,'
                                                                    '"maxTeamMembers": 5,'
                                                                    '"signUpAttachmentUrl": "None",'
                                                                    '"level": 0,'
                                                                    '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Sign up start time must not be later then end time.')

    def test_post_contest_detail_failed_by_wrong_level(self):
        found = resolve('/contest/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"name":"test",'
                                                                    '"description":"test",'
                                                                    '"logoUrl": "None",'
                                                                    '"bannerUrl":"None",'
                                                                    '"signUpStart":"2017-12-31 04:00:54",'
                                                                    '"signUpEnd": "2017-12-31 04:00:55",'
                                                                    '"availableSlots": 0,'
                                                                    '"maxTeamMembers": 5,'
                                                                    '"signUpAttachmentUrl": "None",'
                                                                    '"level": "abcd",'
                                                                    '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Level should be a number.')

    def test_post_contest_detail_failed_by_wrong_level_range(self):
        found = resolve('/contest/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"name":"test",'
                                                                    '"description":"test",'
                                                                    '"logoUrl": "None",'
                                                                    '"bannerUrl":"None",'
                                                                    '"signUpStart":"2017-12-31 04:00:54",'
                                                                    '"signUpEnd": "2017-12-31 04:00:55",'
                                                                    '"availableSlots": 0,'
                                                                    '"maxTeamMembers": 5,'
                                                                    '"signUpAttachmentUrl": "None",'
                                                                    '"level": 128,'
                                                                    '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Level exceeds the range limit.')

    def test_post_remove_contest_successfully(self):
        found = resolve('/contest/remove', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + '}')
        request.user = User.objects.get(username='1')
        found.func(request)
        self.assertEqual(Contest.objects.get(name='test').status, Contest.REMOVED)

    def test_post_batch_remove_contest_successfully(self):
        found = resolve('/contest/batch_remove', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str([Contest.objects.get(name='test').id, ])
        request.body.decode = Mock(return_value='{"contest_id":' + str_id + '}')
        request.user = User.objects.get(username='1')
        found.func(request)
        self.assertEqual(Contest.objects.get(name='test').status, Contest.REMOVED)


class TestPeriodCreate(TestCase):

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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 2,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        found.func(request)

    def test_post_create_period_successfully(self):
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period_0",'
                                                                    '"description":"test_period_0",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":1,'
                                                                    '"name":"test_period_1",'
                                                                    '"description":"test_period_1",'
                                                                    '"startTime":"2017-12-31 06:00:56",'
                                                                    '"endTime": "2017-12-31 06:00:57",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        found.func(request)
        self.assertEqual(Period.objects.get(name='test_period_1').description, 'test_period_1')

    def test_post_create_period_failed_by_end_earlier_than_start(self):
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:56",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Period start time must not be later then end time.')

    def test_post_create_period_failed_by_index_already_taken(self):
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:56",'
                                                                    '"endTime": "2017-12-31 06:00:57",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'The index has been taken by another period.')

    def test_post_create_period_failed_by_time_conflict_earlier(self):
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:56",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":1,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:56",'
                                                                    '"endTime": "2017-12-31 06:00:57",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'].startswith('The new period\'s start time'), True)

    def test_post_create_period_failed_by_time_conflict_later(self):
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":1,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:53",'
                                                                    '"endTime": "2017-12-31 06:00:54",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'].startswith('The new period\'s end time'), True)


class TestPeriods(TestCase):

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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 1,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)

    def test_get_period_successfully(self):
        found = resolve('/period/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        str_id = str(Period.objects.get(name='test_period').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + '}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data']['name'], 'test_period')

    def test_get_period_detail_failed_by_period_not_exist(self):
        found = resolve('/period/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id":10086}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'No Such Period')

    def test_post_period_detail_successfully(self):
        found = resolve('/period/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Period.objects.get(name='test_period').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period0",'
                                                                    '"description":"test_period0",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 3,'
                                                                    '"attachmentUrl": "None",'
                                                                    '"questionId":""}')
        request.user = User.objects.get(username='1')
        found.func(request)
        self.assertEqual(Period.objects.get(id=int(str_id)).name, 'test_period0')

    def test_post_contest_detail_failed_by_wrong_level(self):
        found = resolve('/contest/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"name":"test",'
                                                                    '"description":"test",'
                                                                    '"logoUrl": "None",'
                                                                    '"bannerUrl":"None",'
                                                                    '"signUpStart":"2017-12-31 04:00:54",'
                                                                    '"signUpEnd": "2017-12-31 04:00:55",'
                                                                    '"availableSlots": 0,'
                                                                    '"maxTeamMembers": 5,'
                                                                    '"signUpAttachmentUrl": "None",'
                                                                    '"level": "abcd",'
                                                                    '"tags": "test"}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Level should be a number.')

    def test_post_remove_period_successfully(self):
        found = resolve('/period/remove', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Period.objects.get(name='test_period').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + '}')
        request.user = User.objects.get(username='1')
        found.func(request)
        self.assertEqual(Period.objects.get(name='test_period').status, Period.REMOVED)


class TestQuestionCreate(TestCase):

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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 1,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 2,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)

    def test_post_create_question_successfully(self):
        found = resolve('/question/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Period.objects.get(name='test_period').id)
        request.body.decode = Mock(return_value='{"periodId":' + str_id + ','
                                                                          '"index":0,'
                                                                          '"description":"test_question_0",'
                                                                          '"submissionLimit":0,'
                                                                          '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        request.body.decode = Mock(return_value='{"periodId":' + str_id + ','
                                                                          '"index":1,'
                                                                          '"description":"test_question_1",'
                                                                          '"submissionLimit":0,'
                                                                          '"attachmentUrl": "None"}')
        found.func(request)
        self.assertEqual(ExamQuestion.objects.get(description='test_question_1').description, 'test_question_1')

    def test_post_create_question_failed_by_exceeding_the_limit_of_slots(self):
        found = resolve('/question/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Period.objects.get(name='test_period').id)
        request.body.decode = Mock(return_value='{"periodId":' + str_id + ','
                                                                          '"index":0,'
                                                                          '"description":"test_question_0",'
                                                                          '"submissionLimit":0,'
                                                                          '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        request.body.decode = Mock(return_value='{"periodId":' + str_id + ','
                                                                          '"index":1,'
                                                                          '"description":"test_question_1",'
                                                                          '"submissionLimit":0,'
                                                                          '"attachmentUrl": "None"}')
        found.func(request)
        request.body.decode = Mock(return_value='{"periodId":' + str_id + ','
                                                                          '"index":2,'
                                                                          '"description":"test_question_2",'
                                                                          '"submissionLimit":0,'
                                                                          '"attachmentUrl": "None"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'This period cannot hold more questions.')

    def test_post_create_question_failed_by_index_already_taken(self):
        found = resolve('/question/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Period.objects.get(name='test_period').id)
        request.body.decode = Mock(return_value='{"periodId":' + str_id + ','
                                                                          '"index":0,'
                                                                          '"description":"test_question_0",'
                                                                          '"submissionLimit":0,'
                                                                          '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        request.body.decode = Mock(return_value='{"periodId":' + str_id + ','
                                                                          '"index":0,'
                                                                          '"description":"test_question_1",'
                                                                          '"submissionLimit":0,'
                                                                          '"attachmentUrl": "None"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'The index has been taken by another question.')


class TestQuestions(TestCase):

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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 1,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 1,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        found = resolve('/question/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Period.objects.get(name='test_period').id)
        request.body.decode = Mock(return_value='{"periodId":' + str_id + ','
                                                                          '"index":0,'
                                                                          '"description":"test_question",'
                                                                          '"submissionLimit":0,'
                                                                          '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)

    def test_get_question_successfully(self):
        found = resolve('/question/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        str_id = str(ExamQuestion.objects.get(description='test_question').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + '}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data']['description'], 'test_question')

    def test_get_question_detail_failed_by_question_not_exist(self):
        found = resolve('/question/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id":10086}')
        request.user = User.objects.get(username='1')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'No Such Exam Question')

    def test_post_question_detail_successfully(self):
        found = resolve('/question/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(ExamQuestion.objects.get(description='test_question').id)
        str_pid = str(Period.objects.get(name='test_period').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                '"periodId":' + str_pid + ','
                                                '"index":0,'
                                                '"description":"test_question_0",'
                                                '"submissionLimit":0,'
                                                '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='1')
        found.func(request)
        self.assertEqual(ExamQuestion.objects.get(id=int(str_id)).description, 'test_question_0')

    def test_post_remove_question_successfully(self):
        found = resolve('/question/remove', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(ExamQuestion.objects.get(description='test_question').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + '}')
        request.user = User.objects.get(username='1')
        found.func(request)
        self.assertEqual(ExamQuestion.objects.get(description='test_question').status, ExamQuestion.REMOVED)


class TestTeam(TestCase):

    def setUp(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"test_organizer", "password":"123456",'
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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 1,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='test_organizer')
        found.func(request)
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 1,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='test_organizer')
        found.func(request)
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"test_player", "password":"123456",'
                                                '"gender": "male",'
                                                '"birthday":"2017-11-11",'
                                                '"playerType":0,'
                                                '"email":"",'
                                                '"group":""}')
        found.func(request)
        team = Team.objects.create(name='test_team',
                                   leader=Player.objects.get(gender=True),
                                   contest= Contest.objects.get(name='test'),
                                   avatar_url='',
                                   description='',
                                   sign_up_attachment_url='',
                                   status=Team.CREATING)
        team.members.add(Player.objects.get(gender=True))
        team.save()

    def test_get_team_detail_successfully(self):
        found = resolve('/contest/team/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        str_id = str(Team.objects.get(name='test_team').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + '}')
        request.user = User.objects.get(username='test_organizer')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data']['name'], 'test_team')

    def test_post_team_detail_successfully(self):
        found = resolve('/contest/team/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Team.objects.get(name='test_team').id)
        str_lid = str(Player.objects.get(gender=True).user.id)
        str_pid = str(Period.objects.get(name='test_period').id)
        str_mid = str([Player.objects.get(gender=True).user.id,])
        str_ps = str([])
        request.body.decode = Mock(return_value='{"tid":' + str_id + ','
                                                '"name": "test_team_2",'
                                                '"leaderId": '+str_lid+','
                                                '"memberIds": '+str_mid+','
                                                '"avatarUrl":"",'
                                                '"description":"",'
                                                '"signUpAttachmentUrl":"",'
                                                '"periodId":'+str_pid+','
                                                '"status": 1,'
                                                '"periods":'+str_ps+'}')
        request.user = User.objects.get(username='test_organizer')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

class TestAppeal(TestCase):

    def setUp(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"test_organizer", "password":"123456",'
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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 1,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='test_organizer')
        found.func(request)
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 1,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='test_organizer')
        found.func(request)
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"test_player", "password":"123456",'
                                                '"gender": "male",'
                                                '"birthday":"2017-11-11",'
                                                '"playerType":0,'
                                                '"email":"",'
                                                '"group":""}')
        found.func(request)
        team = Team.objects.create(name='test_team',
                                   leader=Player.objects.get(gender=True),
                                   contest= Contest.objects.get(name='test'),
                                   avatar_url='',
                                   description='',
                                   sign_up_attachment_url='',
                                   status=Team.CREATING)
        team.members.add(Player.objects.get(gender=True))
        team.save()
        appeal = Appeal()
        appeal.initiator = team
        appeal.target_contest = Contest.objects.get(name='test')
        appeal.title = 'test_appeal'
        appeal.content=''
        appeal.attachment_url = ''
        appeal.type = 0
        appeal.status = 0
        appeal.save()

    def test_get_appeal_list_successfully(self):
        found = resolve('/appeal/list', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"cid":' + str_id + '}')
        request.user = User.objects.get(username='test_organizer')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data'][0], 1)

    def test_post_appeal_list_successfully(self):
        found = resolve('/appeal/list', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str([Appeal.objects.get(title='test_appeal').id,])
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                '"status":0}')
        request.user = User.objects.get(username='test_organizer')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

    def test_get_appeal_detail_successfully(self):
        found = resolve('/appeal/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + '}')
        request.user = User.objects.get(username='test_organizer')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data']['title'], 'test_appeal')

    def test_post_appeal_detail_successfully(self):
        found = resolve('/appeal/detail', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Appeal.objects.get(title='test_appeal').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                '"status":0}')
        request.user = User.objects.get(username='test_organizer')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


class TestBatchTeamMannage(TestCase):

    def setUp(self):
        found = resolve('/register', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"test_organizer", "password":"123456",'
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
                                                '"signUpStart":"2017-12-31 04:00:54",'
                                                '"signUpEnd": "2017-12-31 04:00:55",'
                                                '"availableSlots": 1,'
                                                '"maxTeamMembers": 5,'
                                                '"signUpAttachmentUrl": "None",'
                                                '"level": 0,'
                                                '"tags": "test"}')
        request.user = User.objects.get(username='test_organizer')
        found.func(request)
        found = resolve('/period/create', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"id":' + str_id + ','
                                                                    '"index":0,'
                                                                    '"name":"test_period",'
                                                                    '"description":"test_period",'
                                                                    '"startTime":"2017-12-31 06:00:54",'
                                                                    '"endTime": "2017-12-31 06:00:55",'
                                                                    '"availableSlots": 1,'
                                                                    '"attachmentUrl": "None"}')
        request.user = User.objects.get(username='test_organizer')
        found.func(request)
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"test_player", "password":"123456",'
                                                '"gender": "male",'
                                                '"birthday":"2017-11-11",'
                                                '"playerType":0,'
                                                '"email":"",'
                                                '"group":""}')
        found.func(request)
        team = Team.objects.create(name='test_team',
                                   leader=Player.objects.get(gender=True),
                                   contest= Contest.objects.get(name='test'),
                                   avatar_url='',
                                   description='',
                                   sign_up_attachment_url='',
                                   status=Team.CREATING)
        team.members.add(Player.objects.get(gender=True))
        team.save()

    def test_get_team_all_successfully(self):
        found = resolve('/contest/team_batch_manage', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        str_id = str(Contest.objects.get(name='test').id)
        request.body.decode = Mock(return_value='{"cid":' + str_id + '}')
        request.user = User.objects.get(username='test_organizer')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['data'][0]['id'], 1)

    def test_post_team_all_successfully(self):
        found = resolve('/contest/team_batch_manage', urlconf=organizerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        str_id = str([Team.objects.get(name='test_team').id,])
        request.body.decode = Mock(return_value='{"teamId":' + str_id + ','
                                                '"status":0}')
        request.user = User.objects.get(username='test_organizer')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

