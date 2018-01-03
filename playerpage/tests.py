from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from unittest.mock import Mock, patch
from test_me_app.models import *
import playerpage.urls
import organizerpage.urls
import json

# Create your tests here.


class TestPlayerRegister(TestCase):

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
                                                '"gender":"female", "playerType":1, "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


class TestPlayerPersonalInfo(TestCase):

    def test_personal_info_get_player_required(self):
        found = resolve('/personal_info', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET',
                       user=Mock(is_authenticated=True, user_type=User_profile.ORGANIZER))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 3)
        self.assertEqual(response['msg'], 'Player required')

    def test_personal_info_post_wrong_phone(self):
        found = resolve('/personal_info', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST',
                       user=Mock(is_authenticated=True, user_type=User_profile.PLAYER))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"email":"1@1.com", "group":"test_group",'
                                                '"nickname":"test_nick", "avatarUrl":"test_url",'
                                                '"contactPhone":"130abcd1234", "description":"test_des",'
                                                '"gender":"male", "birthday":"2000-01-01", "playerType":0 }')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['msg'], 'Wrong contact phone')


class TestAppealCreate(TestCase):

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

    def test_post_create_appeal_successfully(self):
        found = resolve('/appeal/create', urlconf = playerpage.urls)
        request = Mock(wraps=HttpRequest(), method = 'POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name="test").id)
        request.body.decode = Mock(return_value='{"contestId":'+str_id+','
                                                '"title":"test_appeal",'
                                                '"content": "test_appeal_0",'
                                                '"attachmentUrl":"None"}')
        request.user = User.objects.get(username='2')
        found.func(request)


class TestAppeal(TestCase):

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
        found = resolve('/appeal/create', urlconf = playerpage.urls)
        request = Mock(wraps=HttpRequest(), method = 'POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name="test").id)
        request.body.decode = Mock(return_value='{"contestId":'+str_id+','
                                                '"title":"test_appeal_0",'
                                                '"content": "test_appeal_0",'
                                                '"attachmentUrl":"None"}')
        request.user = User.objects.get(username='2')
        found.func(request)
        found = resolve('/appeal/create', urlconf = playerpage.urls)
        request = Mock(wraps=HttpRequest(), method = 'POST')
        request.body = Mock()
        str_id = str(Contest.objects.get(name="test").id)
        request.body.decode = Mock(return_value='{"contestId":'+str_id+','
                                                '"title":"test_appeal_1",'
                                                '"content": "test_appeal_1",'
                                                '"attachmentUrl":"None"}')
        request.user = User.objects.get(username='2')
        found.func(request)

    def test_get_appeal_list_successfully(self):
        found = resolve('/appeal/list', urlconf = playerpage.urls)
        request = Mock(wraps = HttpRequest(), method = 'GET')
        request.body = Mock()
        str_id = str(Contest.objects.get(name="test").id)
        request.body.decode = Mock(return_value='{"cid":'+str_id+'}')
        request.user = User.objects.get(username='2')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(len(response['data']), 2)

    def test_get_appeal_list_failed_by_no_such_contest(self):
        found = resolve('/appeal/list', urlconf = playerpage.urls)
        request = Mock(wraps = HttpRequest(), method = 'GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"cid":10086}')
        request.user = User.objects.get(username='2')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'No Such Contest')

    def test_get_appeal_detail_successfully(self):
        found = resolve('/appeal/detail', urlconf = playerpage.urls)
        request = Mock(wraps = HttpRequest(), method = 'GET')
        request.body = Mock()
        str_id = str(Appeal.objects.get(title="test_appeal_0").id)
        request.body.decode = Mock(return_value='{"id":'+str_id+'}')
        request.user = User.objects.get(username='2')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

    def test_get_appeal_detail_failed_by_no_such_appeal(self):
        found = resolve('/appeal/detail', urlconf = playerpage.urls)
        request = Mock(wraps = HttpRequest(), method = 'GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id":10086}')
        request.user = User.objects.get(username='2')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'No Such Appeal')

    def test_post_appeal_detail_successfully(self):
        found = resolve('/appeal/detail', urlconf = playerpage.urls)
        request = Mock(wraps = HttpRequest(), method = 'POST')
        request.body = Mock()
        str_id = str(Appeal.objects.get(title="test_appeal_0").id)
        str_cid = str(Contest.objects.get(name="test").id)
        request.body.decode = Mock(return_value='{"id":'+str_id+','
                                                '"contestId":'+str_cid+','
                                                '"title":"test_appeal_1",'
                                                '"content": "test_appeal_1",'
                                                '"attachmentUrl":"None",'
                                                '"status":0}')
        request.user = User.objects.get(username='2')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

    def test_post_appeal_detail_failed_by_status_not_a_num(self):
        found = resolve('/appeal/detail', urlconf = playerpage.urls)
        request = Mock(wraps = HttpRequest(), method = 'POST')
        request.body = Mock()
        str_id = str(Appeal.objects.get(title="test_appeal_0").id)
        str_cid = str(Contest.objects.get(name="test").id)
        request.body.decode = Mock(return_value='{"id":'+str_id+','
                                                '"contestId":'+str_cid+','
                                                '"title":"test_appeal_1",'
                                                '"content": "test_appeal_1",'
                                                '"attachmentUrl":"None",'
                                                '"status":"test"}')
        request.user = User.objects.get(username='2')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'The field status should be a number.')

    def test_post_appeal_detail_failed_by_status_exceeding_range(self):
        found = resolve('/appeal/detail', urlconf = playerpage.urls)
        request = Mock(wraps = HttpRequest(), method = 'POST')
        request.body = Mock()
        str_id = str(Appeal.objects.get(title="test_appeal_0").id)
        str_cid = str(Contest.objects.get(name="test").id)
        request.body.decode = Mock(return_value='{"id":'+str_id+','
                                                '"contestId":'+str_cid+','
                                                '"title":"test_appeal_1",'
                                                '"content": "test_appeal_1",'
                                                '"attachmentUrl":"None",'
                                                '"status":10086}')
        request.user = User.objects.get(username='2')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['msg'], 'Status exceeds supposed range.')

    def test_post_remove_appeal_successfully(self):
        found = resolve('/appeal/remove', urlconf = playerpage.urls)
        request = Mock(wraps = HttpRequest(), method = 'POST')
        request.body = Mock()
        str_id = str(Appeal.objects.get(title="test_appeal_0").id)
        request.body.decode = Mock(return_value='{"id":'+str_id+'}')
        request.user = User.objects.get(username='2')
        found.func(request)
        self.assertEqual(Appeal.objects.get(title="test_appeal_0").status, Appeal.REMOVED)
