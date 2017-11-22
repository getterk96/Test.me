from django.core.exceptions import ObjectDoesNotExist
from codex.baseerror import *
from codex.baseview import APIView
from codex.basedecorator import *
from test_me_app.models import *
from test_me import settings
import time, datetime

# Create your views here.


def check_gender(gender):
    if gender not in ['male', 'female']:
        raise InputError('Wrong gender')


def check_player_type(player_type):
    if player_type < 0 or player_type > 4:
        raise InputError('Wrong player type')


def check_contact_phone(contact_phone):
    for c in contact_phone:
        if c < '0' or c > '9':
            raise InputError('Wrong contact phone')


class PlayerRegister(APIView):

    def post(self):
        # check
        self.check_input('username', 'password', 'email', 'group', 'gender', 'playerType', 'birthday')
        check_gender(self.input['gender'])
        check_player_type(self.input['playerType'])
        # create
        try:
            user = User.objects.create_user(username=self.input['username'],
                                            password=self.input['password'],
                                            email=self.input['email'])
            user.user_type = User_profile.PLAYER
            user.save()
            # default columns
            avatar_url = settings.get_url(settings.STATIC_URL + 'img/default_avatar.jpg')
            description = '这个人很懒，什么都没有留下'
            # create player
            player = Player.objects.create(user=user,
                                           nickname=self.input['username'],
                                           group=self.input['group'],
                                           avatar_url=avatar_url,
                                           description=description,
                                           gender=(self.input['gender'] == 'male'),
                                           player_type=self.input['playerType'],
                                           birthday=self.input['birthday'])
            player.save()
        except:
            raise LogicError('Signup fail')


class PlayerPersonalInfo(APIView):

    @player_required
    def get(self):
        player = self.request.user.player
        return {
            'username': self.request.user.username,
            'email': self.request.user.email,
            'group': player.group,
            'nickname': player.nickname,
            'avatarUrl': player.avatar_url,
            'contactPhone': player.contact_phone,
            'description': player.description,
            'gender': 'male' if player.gender else 'female',
            'birthday': player.birthday,
            'playerType': player.player_type
        }

    @player_required
    def post(self):
        # check
        self.check_input('email', 'group', 'nickname', 'avatarUrl', 'contactPhone',
                         'description', 'gender', 'birthday', 'playerType')
        check_contact_phone(self.input['contactPhone'])
        check_gender(self.input['gender'])
        check_player_type(self.input['playerType'])
        # change
        player = self.request.player
        self.request.user.email = self.input['email']
        player.group = self.input['group']
        player.nickname = self.input['nickname']
        player.avatar_url = self.input['avatarUrl']
        player.contact_phone = self.input['contactPhone']
        player.description = self.input['description']
        player.gender = (self.input['gender'] == 'male')
        player.birthday = self.input['gender']
        player.player_type = self.input['playerType']
        player.save()


class PlayerParticipatingContests(APIView):

    @player_required
    def get(self):
        player = self.request.user.player
        contests = []
        for team in (player.lead_teams + player.join_teams):
            contests.append({'id': team.contest.id,
                             'name': team.contest.name,
                             'organizerName': team.contest.organizer.nickname})
        return contests


class PlayerContestDetail(APIView):

    @player_required
    def get(self):
        # check
        self.check_input('cid')
        try:
            contest = Contest.objects.get(id=self.input['cid'])
        except ObjectDoesNotExist:
            raise InputError('Contest does not exist')

        # already sign up
        player = self.request.user.player
        already_signup = False
        for team in (player.lead_teams + player.join_teams):
            if team.contest == contest:
                already_signup = True
        # tags
        tags = []
        for tag in contest.tags:
            tags.append(tag.content)
        # periods
        periods = []
        for period in contest.period_set:
            periods.append({'periodName': period.name,
                            'periodId': period.id,
                            'periodSlots': period.available_slots,
                            'periodStartTime': time.mktime(period.start_time.timetumple()),
                            'periodEndTime': time.mktime(period.end_time.timetumple())})

        return {
            'name': contest.name,
            'description': contest.description,
            'logoUrl': contest.logo_url,
            'bannerUrl': contest.banner_url,
            'alreadySignUp': already_signup,
            'signUpStartTime': time.mktime(contest.sign_up_start_time.timetuple()),
            'signUpEndTime': time.mktime(contest.sign_up_end_time.timetuple()),
            'currentTime': time.mktime(datetime.datetime.now().timetuple()),
            'availableSlots': contest.available_slots,
            'maxTeamMembers': contest.max_team_members,
            'signUpAttachmentUrl': contest.sign_up_attachment_url,
            'level': contest.level,
            'tags': tags,
            'periods': periods
        }
