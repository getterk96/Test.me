from django.test import TestCase
from django.core import management
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from unittest.mock import Mock
from test_me_app.models import *
import playerpage.urls
import json

# Create your tests here.


def load_test_database():
    management.call_command('loaddata', 'user.json', verbosity=0)
    management.call_command('loaddata', 'user_profile.json', verbosity=0)
    management.call_command('loaddata', 'player.json', verbosity=0)
    management.call_command('loaddata', 'organizer.json', verbosity=0)
    management.call_command('loaddata', 'contest.json', verbosity=0)
    management.call_command('loaddata', 'team.json', verbosity=0)


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

    @classmethod
    def setUpClass(cls):
        load_test_database()

    @classmethod
    def tearDownClass(cls):
        management.call_command('flush', verbosity=0, interactive=False)

    def test_player_required(self):
        found = resolve('/personal_info', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET',
                       user=Mock(is_authenticated=True,
                                 user_profile=Mock(user_type=User_profile.ORGANIZER,
                                                   status=User_profile.NORMAL)))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 3)
        self.assertEqual(response['msg'], 'Player required')

    def test_personal_info_get(self):
        found = resolve('/personal_info', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('email'), '1@test.me')
        self.assertEqual(response['data'].get('nickname'), 'nickname1')

    def test_personal_info_post_wrong_input(self):
        found = resolve('/personal_info', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"email":"1@1.com", "group":"test_group",'
                                                '"nickname":"test_nick", "avatarUrl":"test_url",'
                                                '"contactPhone":"130abcd1234", "description":"test_des",'
                                                '"gender":"male", "birthday":"2000-01-01", "playerType":0 }')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['msg'], 'Wrong contact phone')

    def test_personal_info_post_success(self):
        found = resolve('/personal_info', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"email":"1@1.com", "group":"test_group",'
                                                '"nickname":"test_nick", "avatarUrl":"test_url",'
                                                '"contactPhone":"13000000000", "description":"test_des",'
                                                '"gender":"male", "birthday":"2000-01-01", "playerType":0 }')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


class TestPlayerParticipatingContests(TestCase):

    @classmethod
    def setUpClass(cls):
        load_test_database()

    @classmethod
    def tearDownClass(cls):
        management.call_command('flush', verbosity=0, interactive=False)

    def test_participating_contests_get(self):
        found = resolve('/participating_contests', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'][0].get('id'), 1)
