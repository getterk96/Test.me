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
        management.call_command('loaddata', 'adminpage/fixtures/contest.json', verbosity=0)
        management.call_command('loaddata', 'adminpage/fixtures/appeal.json', verbosity=0)

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


class TestAdminUserSearch(AdminPageTestCase):

    def test_user_search_get_exist(self):
        found = resolve('/user/search', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username": "name2", "userType": 0}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['data'][0].get('id'), 2)

    def test_user_search_get_not_exist(self):
        found = resolve('/user/search', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username": "name233", "userType": 0}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(len(response['data']), 0)


class TestAdminUserDelete(AdminPageTestCase):

    def test_user_delete_post_success(self):
        found = resolve('/user/delete', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"ids":[2, 3]}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(User.objects.get(id=2).user_profile.status, User_profile.CANCELED)


class TestAdminUserRecover(AdminPageTestCase):

    def test_user_recover_post(self):
        found = resolve('/user/recover', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        user = User.objects.get(id=2)
        user.user_profile.status = User_profile.CANCELED
        user.user_profile.save()
        request.body.decode = Mock(return_value='{"ids":[2]}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(User.objects.get(id=2).user_profile.status, User_profile.NORMAL)


class TestAdminPlayerDetail(AdminPageTestCase):

    def test_player_detail_get(self):
        found = resolve('/player/detail', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id": 2}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('nickname'), 'nickname1')
        self.assertEqual(response['data'].get('gender'), 'female')

    def test_player_detail_post(self):
        found = resolve('/player/detail', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id": 2, "email": "233@test.me",'
                                                '"group": "group233", "nickname":"nickname233",'
                                                '"avatarUrl":"avatarUrl233", "contactPhone":"233",'
                                                '"description":"description", "gender":"male",'
                                                '"birthday":"2008-01-01","playerType":2}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        player = User.objects.get(id=2).player
        self.assertEqual(player.group, "group233")
        self.assertEqual(player.gender, 1)


class TestAdminOrganizerDetail(AdminPageTestCase):

    def test_organizer_detail_get(self):
        found = resolve('/organizer/detail', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id": 3}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('nickname'), 'nickname1')
        self.assertEqual(response['data'].get('verifyUrl'), 'verify_file_url1')

    def test_organizer_detail_post(self):
        found = resolve('/organizer/detail', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id": 3, "email": "3@test.me",'
                                                '"group": "group123", "nickname": "nickname123",'
                                                '"avatarUrl":"avatarUrl123", "description":"description123",'
                                                '"contactPhone":"123", "verifyUrl":"verifyUrl123"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        organizer = User.objects.get(id=3).organizer
        self.assertEqual(organizer.avatar_url, "avatarUrl123")


class TestAdminOrganizerVerification(AdminPageTestCase):

    def test_organizer_verification_post_verified(self):
        found = resolve('/organizer/verification', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id":3, "verify":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(User.objects.get(id=3).organizer.verify_status, Organizer.VERIFIED)

    def test_organizer_verification_post_rejected(self):
        found = resolve('/organizer/verification', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id":3, "verify":0}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(User.objects.get(id=3).organizer.verify_status, Organizer.REJECTED)


class TestAdminContestList(AdminPageTestCase):

    def test_contest_list_get(self):
        found = resolve('/contest/list', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['data'][0].get('contestName'), 'publish_contest')


class TestAdminContestSearch(AdminPageTestCase):

    def test_contest_search_get_not_exist(self):
        found = resolve('/contest/search', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"contestName": "aaa", "organizerName": "nickname"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(len(response['data']), 0)

    def test_contest_search_get_exist(self):
        found = resolve('/contest/search', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"contestName": "_contes", "organizerName": "nick"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['data'][0].get('id'), 1)


class TestAdminContestDetail(AdminPageTestCase):

    def test_contest_detail_get(self):
        found = resolve('/contest/detail', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"cid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('name'), 'publish_contest')

    def test_contest_detail_post(self):
        found = resolve('/contest/detail', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"cid":1, "name":"contest233", "organizerId":1,'
                                                '"description":"description233", "logoUrl":"logoUrl233",'
                                                '"bannerUrl":"bannerUrl233", "signUpStartTime":"2017-01-01 00:00:00",'
                                                '"signUpEndTime":"2017-01-03 00:00:00", "availableSlots": 200,'
                                                '"maxTeamMembers": 20, "signUpAttachmentUrl": "url233",'
                                                '"level":1, "tags":"tag1,tag2"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(Contest.objects.get(id=1).name, 'contest233')
        self.assertEqual(Contest.objects.get(id=1).tags.count(), 2)


class TestAdminContestVerification(AdminPageTestCase):

    def test_contest_verification_post_publish(self):
        found = resolve('/contest/verification', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"cid":1, "verify":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(Contest.objects.get(id=1).status, Contest.PUBLISHED)

    def test_contest_verification_post_cancel(self):
        found = resolve('/contest/verification', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"cid":1, "verify":0}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(Contest.objects.get(id=1).status, Contest.CANCELLED)


class TestAdminAppealDetail(AdminPageTestCase):

    def test_appeal_detail_get(self):
        found = resolve('/appeal/detail', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('content'), 'content1')

    def test_appeal_detail_post(self):
        found = resolve('/appeal/detail', urlconf=adminpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"id":1, "contestId": 1,'
                                                '"title":"title233", "content":"content233",'
                                                '"attachmentUrl":"attachmentUrl233",'
                                                '"status":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(Appeal.objects.get(id=1).title, 'title233')
