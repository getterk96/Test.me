from django.test import TransactionTestCase
from django.core import management
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from unittest.mock import Mock, patch
from test_me_app.models import *
import playerpage.urls
import json
import datetime

# Create your tests here.


def load_test_database():
    management.call_command('loaddata', 'user.json', verbosity=0)
    for user in User.objects.all():
        user.user_profile.delete()
    management.call_command('loaddata', 'user_profile.json', verbosity=0)
    management.call_command('loaddata', 'player.json', verbosity=0)
    management.call_command('loaddata', 'organizer.json', verbosity=0)
    management.call_command('loaddata', 'tag.json', verbosity=0)
    management.call_command('loaddata', 'contest.json', verbosity=0)
    management.call_command('loaddata', 'period.json', verbosity=0)
    management.call_command('loaddata', 'team.json', verbosity=0)
    management.call_command('loaddata', 'periodscore.json', verbosity=0)
    management.call_command('loaddata', 'examquestion.json', verbosity=0)
    management.call_command('loaddata', 'work.json', verbosity=0)
    management.call_command('loaddata', 'teaminvitation.json', verbosity=0)


class PlayerPageTestCase(TransactionTestCase):

    def setUp(self):
        load_test_database()

    def tearDown(self):
        management.call_command('flush', verbosity=0, interactive=False)


class TestPlayerRegister(PlayerPageTestCase):

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

    def test_register_duplicate_username(self):
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"username1", "password":"3",'
                                                '"email":"2@2.com", "group": "test_group",'
                                                '"gender":"female", "playerType":1, "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Signup fail')

    def test_register_success(self):
        found = resolve('/register', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"new_username", "password":"3",'
                                                '"email":"2@2.com", "group": "test_group",'
                                                '"gender":"female", "playerType":1, "birthday":"2017-11-23"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


class TestPlayerPersonalInfo(PlayerPageTestCase):

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


class TestPlayerParticipatingContests(PlayerPageTestCase):

    def test_participating_contests_get(self):
        found = resolve('/participating_contests', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'][0].get('id'), 1)
        self.assertEqual(response['data'][0].get('name'), 'publish_contest')
        self.assertEqual(response['data'][0].get('organizerName'), 'nickname1')


class TestPlayerContestDetail(PlayerPageTestCase):

    def test_player_contest_detail_get_signuped(self):
        found = resolve('/contest/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"cid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('name'), 'publish_contest')
        self.assertEqual(response['data'].get('tags')[0], 'tag1')
        self.assertEqual(response['data'].get('periods')[0].get('periodName'), 'period1')
        self.assertEqual(response['data'].get('alreadySignUp'), 1)

    def test_player_contest_detail_get_unsignuped(self):
        found = resolve('/contest/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=3))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"cid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('alreadySignUp'), 0)


class TestPlayerContestSearchSimple(PlayerPageTestCase):

    def test_contest_search_simple_get_has_result(self):
        found = resolve('/contest/search/simple', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"keyword":"contest"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'][0].get('id'), 1)

    def test_contest_search_simple_get_no_result(self):
        found = resolve('/contest/search/simple', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"keyword":"word"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(len(response['data']), 0)


class TestPlayerPeriodDetail(PlayerPageTestCase):

    def test_period_detail_get_unsignuped(self):
        found = resolve('/period/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=3))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"pid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'You have not sign up this contest')

    def test_period_detail_get_no_score(self):
        found = resolve('/period/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"pid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('name'), 'period1')
        self.assertEqual(response['data'].get('score'), -1)

    def test_period_detail_get_scored(self):
        found = resolve('/period/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=4))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"pid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('score'), 100)


class TestPlayerQuestionDetail(PlayerPageTestCase):

    def test_question_detail_get_no_submit(self):
        found = resolve('/question/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"pid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'][0].get('id'), 1)
        self.assertEqual(response['data'][0].get('submission_times'), 0)

    def test_question_detail_get_submitted(self):
        found = resolve('/question/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=4))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"pid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'][0].get('submission_times'), 3)


class TestPlayerQuestionSubmit(PlayerPageTestCase):

    def test_question_submit_post_not_in_period(self):
        found = resolve('/question/submit', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"qid":1, "workUrl":"work1"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'You can not submit for this question')

    def test_question_submit_post_wrong_time(self):
        found = resolve('/question/submit', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=4))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"qid":1, "workUrl":"work1"}')
        period = Period.objects.get(id=1)
        period.start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        period.end_time = datetime.datetime.now() + datetime.timedelta(days=-1)
        period.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Can not submit now')

    def test_question_submit_post_not_leader(self):
        found = resolve('/question/submit', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=5))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"qid":1, "workUrl":"work1"}')
        period = Period.objects.get(id=1)
        period.start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        period.end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        period.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Only team leader can submit work')

    def test_question_submit_post_submit_over_times(self):
        found = resolve('/question/submit', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=4))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"qid":1, "workUrl":"work1"}')
        period = Period.objects.get(id=1)
        period.start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        period.end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        period.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Out of submission limit')

    def test_question_submit_post_success(self):
        found = resolve('/question/submit', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=6))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"qid":1, "workUrl":"work1"}')
        period = Period.objects.get(id=1)
        period.start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        period.end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        period.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


class TestPlayerTeamList(PlayerPageTestCase):

    def test_team_list_get(self):
        found = resolve('/team/list', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'][0].get('name'), 'team1')


class TestPlayerTeamCreate(PlayerPageTestCase):

    def test_team_create_post_wrong_time(self):
        found = resolve('/team/create', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"team233", "members":["username3"],'
                                                '"contestId": 1, "avatarUrl": "avatar_url233",'
                                                '"description": "description233", '
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl233"}')
        contest = Contest.objects.get(id=1)
        contest.sign_up_start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        contest.sign_up_end_time = datetime.datetime.now() + datetime.timedelta(days=-1)
        contest.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Contest is not in sign up time')

    def test_team_create_post_already_signup(self):
        found = resolve('/team/create', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"team233", "members":["username3"],'
                                                '"contestId": 1, "avatarUrl": "avatar_url233",'
                                                '"description": "description233", '
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl233"}')
        contest = Contest.objects.get(id=1)
        contest.sign_up_start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        contest.sign_up_end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        contest.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'You are already in a team of this contest')

    def test_team_create_post_wrong_member(self):
        found = resolve('/team/create', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=7))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"team233", "members":["username_no_exist"],'
                                                '"contestId": 1, "avatarUrl": "avatar_url233",'
                                                '"description": "description233", '
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl233"}')
        contest = Contest.objects.get(id=1)
        contest.sign_up_start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        contest.sign_up_end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        contest.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['msg'], 'Player does not exist')

    def test_team_create_post_too_many_members(self):
        found = resolve('/team/create', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=7))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"team233", "members":["username8", "username9"],'
                                                '"contestId": 1, "avatarUrl": "avatar_url233",'
                                                '"description": "description233", '
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl233"}')
        contest = Contest.objects.get(id=1)
        contest.sign_up_start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        contest.sign_up_end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        contest.max_team_members = 2
        contest.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Number of team member should be no more than 2')

    def test_team_create_post_too_many_teams(self):
        found = resolve('/team/create', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=7))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"team233", "members":["username8", "username9"],'
                                                '"contestId": 1, "avatarUrl": "avatar_url233",'
                                                '"description": "description233", '
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl233"}')
        contest = Contest.objects.get(id=1)
        contest.sign_up_start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        contest.sign_up_end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        contest.available_slots = 3
        contest.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'No more team could sign up, max team number: 3')

    def test_team_create_post_success(self):
        found = resolve('/team/create', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=7))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"name":"team233", "members":["username8", "username9"],'
                                                '"contestId": 1, "avatarUrl": "avatar_url233",'
                                                '"description": "description233", '
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl233"}')
        contest = Contest.objects.get(id=1)
        contest.sign_up_start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        contest.sign_up_end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        contest.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


class TestPlayerTeamDetail(PlayerPageTestCase):

    def test_team_detail_get_not_in(self):
        found = resolve('/team/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":2}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 3)
        self.assertEqual(response['msg'], 'You are not in this team')

    def test_team_detail_get_success(self):
        found = resolve('/team/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'].get('name'), 'team1')

    def test_team_detail_post_not_leader(self):
        found = resolve('/team/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":2, "leaderId": 1, "memberIds":[],'
                                                '"avatarUrl":"avatarUrl1", "description":"description1",'
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl1"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 3)
        self.assertEqual(response['msg'], 'Only team leader can change team info')

    def test_team_detail_post_signed_up(self):
        found = resolve('/team/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":1, "leaderId": 1, "memberIds":[],'
                                                '"avatarUrl":"avatarUrl1", "description":"description1",'
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl1"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Can not modify signed-up team info')

    def test_team_detail_post_too_many_member(self):
        found = resolve('/team/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":1, "leaderId": 1, "memberIds":[3, 4, 5],'
                                                '"avatarUrl":"avatarUrl1", "description":"description1",'
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl1"}')
        team = Team.objects.get(id=1)
        team.status = Team.CREATING
        team.save()
        contest = Contest.objects.get(id=1)
        contest.max_team_members = 2
        contest.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Number of team member should be no more than 2')

    def test_team_detail_post_wrong_member(self):
        found = resolve('/team/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":1, "leaderId": 1, "memberIds":[4],'
                                                '"avatarUrl":"avatarUrl1", "description":"description1",'
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl1"}')
        team = Team.objects.get(id=1)
        team.status = Team.CREATING
        team.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Member username4 is already in another team of this contest')

    def test_team_detail_post_success(self):
        found = resolve('/team/detail', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":1, "leaderId": 1, "memberIds":[3],'
                                                '"avatarUrl":"avatarUrl1", "description":"description1",'
                                                '"signUpAttachmentUrl":"signUpAttachmentUrl1"}')
        team = Team.objects.get(id=1)
        team.status = Team.CREATING
        team.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


class TestPlayerTeamDismiss(PlayerPageTestCase):

    def test_team_dismiss_post_not_leader(self):
        found = resolve('/team/dismiss', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":2}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 3)
        self.assertEqual(response['msg'], 'Only team leader can dismiss team')

    def test_team_dismiss_post_success(self):
        found = resolve('/team/dismiss', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


class TestPlayerTeamInvitation(PlayerPageTestCase):

    def test_team_invitation_get(self):
        found = resolve('/team/invitation', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET', user=User.objects.get(id=5))
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['data'][0].get('teamName'), 'team2')

    def test_team_invitation_post(self):
        found = resolve('/team/invitation', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=5))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"iid":1, "confirm":1}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)
        self.assertEqual(TeamInvitation.objects.get(id=1).status, TeamInvitation.CONFIRMED)


class TestPlayerTeamSignUp(PlayerPageTestCase):

    def test_team_sign_up_post_wrong_time(self):
        found = resolve('/team/signup', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=4))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":2}')
        contest = Contest.objects.get(id=1)
        contest.sign_up_start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        contest.sign_up_end_time = datetime.datetime.now() + datetime.timedelta(days=-1)
        contest.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Contest is not in sign up time')

    def test_team_sign_up_post_not_all_confirmed(self):
        found = resolve('/team/signup', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=4))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":2}')
        contest = Contest.objects.get(id=1)
        contest.sign_up_start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        contest.sign_up_end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        contest.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'Team can sign up until all members confirm')

    def test_team_sign_up_post_success(self):
        found = resolve('/team/signup', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=4))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"tid":2}')
        contest = Contest.objects.get(id=1)
        contest.sign_up_start_time = datetime.datetime.now() + datetime.timedelta(days=-2)
        contest.sign_up_end_time = datetime.datetime.now() + datetime.timedelta(days=2)
        contest.save()
        team_invitation = TeamInvitation.objects.get(id=1)
        team_invitation.status = TeamInvitation.CONFIRMED
        team_invitation.save()
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)


class TestPlayerAppealCreate(PlayerPageTestCase):

    def test_appeal_create_post_contest_not_exist(self):
        found = resolve('/appeal/create', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"contestId": 233, "title":"title1",'
                                                '"content":"content1", "attachmentUrl":"attachmentUrl1"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['msg'], 'No Such Contest')

    def test_appeal_create_post_success(self):
        found = resolve('/appeal/create', urlconf=playerpage.urls)
        request = Mock(wraps=HttpRequest(), method='POST', user=User.objects.get(id=1))
        request.body = Mock()
        request.body.decode = Mock(return_value='{"contestId": 1, "title":"title1",'
                                                '"content":"content1", "attachmentUrl":"attachmentUrl1"}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 0)

