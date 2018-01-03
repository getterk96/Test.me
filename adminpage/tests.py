from django.test import TransactionTestCase
from django.core import management
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from unittest.mock import Mock
from test_me_app.models import *
import adminpage.urls
import json

# Create your tests here.


class AdminPageTestCase(TransactionTestCase):

    def setUp(self):
        management.call_command('loaddata', 'adminpage/fixtures/user.json', verbosity=0)
        for user in User.objects.all():
            user.user_profile.delete()
        management.call_command('loaddata', 'adminpage/fixtures/user_profile.json', verbosity=0)
        management.call_command('loaddata', 'adminpage/fixtures/player.json', verbosity=0)
        management.call_command('loaddata', 'adminpage/fixtures/organizer.json', verbosity=0)

    def tearDown(self):
        management.call_command('flush', verbosity=0, interactive=False)


class TestAdminUserList(AdminPageTestCase):

    def test_admin_required(self):
        found = resolve('/user/list', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=2))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 3)
        self.assertEqual(response['msg'], 'Admin required')

    def test_user_list_get(self):
        found = resolve('/user/list', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(len(response['data']), 3)
        self.assertEqual(response['data'][0].get('id'), 1)

