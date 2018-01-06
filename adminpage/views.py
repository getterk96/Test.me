from codex.baseerror import *
from codex.baseview import APIView
from test_me import settings
from codex.basedecorator import admin_required
from test_me_app.models import *
import time


class AdminRegister(APIView):

    def post(self):
        self.check_input('username', 'password', 'email', 'adminToken')
        if self.input['adminToken'] != settings.ADMIN_TOKEN:
            raise ValidateError('Wrong admin token')
        try:
            user = User.objects.create_user(username=self.input['username'],
                                            password=self.input['password'],
                                            email=self.input['email'])
            user.user_profile.user_type = User_profile.ADMINISTRATOR
            user.save()
            user.user_profile.save()
        except:
            raise LogicError('Sign up fail')
        

class AdminUserList(APIView):

    @admin_required
    def get(self):
        users = []
        for user in User.objects.all():
            users.append({
                'id': user.id,
                'username': user.username,
                'userType': user.user_profile.user_type
            })
        return users


class AdminUserSearch(APIView):

    @admin_required
    def get(self):
        self.check_input('username', 'userType')
        users = []
        for user in User.objects.filter(username__contains=self.input['username'],
                                        user_profile__user_type=self.input['userType']):
            users.append({
                'id': user.id,
                'username': user.username,
                'userType': user.user_profile.user_type
            })
        return users


class AdminUserDelete(APIView):

    @admin_required
    def post(self):
        self.check_input('ids')
        user_list = []
        try:
            for id in self.input['ids']:
                user_list.append(User.objects.get(id=id))
        except ObjectDoesNotExist:
            raise LogicError('No such user')

        for user in user_list:
            user.user_profile.status = User_profile.CANCELED
            user.user_profile.save()


class AdminUserRecover(APIView):

    @admin_required
    def post(self):
        self.check_input('ids')
        user_list = []
        try:
            for id in self.input['ids']:
                user_list.append(User.objects.get(id=id))
        except ObjectDoesNotExist:
            raise LogicError('No such user')

        for user in user_list:
            user.user_profile.status = User_profile.NORMAL
            user.user_profile.save()


class AdminPlayerDetail(APIView):

    @admin_required
    def get(self):
        self.check_input('id')
        try:
            user = User.objects.get(id=self.input['id'], user_profile__user_type=User_profile.PLAYER)
        except ObjectDoesNotExist:
            raise LogicError('No such player')

        player = user.player
        return {
            'username': user.username,
            'email': user.email,
            'group': player.group,
            'nickname': player.nickname,
            'avatarUrl': player.avatar_url,
            'contactPhone': player.contact_phone,
            'description': player.description,
            'gender': 'male' if player.gender else 'female',
            'birthday': player.birthday.strftime("%Y-%m-%d"),
            'playerType': player.player_type
        }

    @admin_required
    def post(self):
        self.check_input('id', 'email', 'group', 'nickname', 'avatarUrl', 'contactPhone',
                         'description', 'gender', 'birthday', 'playerType')
        try:
            user = User.objects.get(id=self.input['id'], user_profile__user_type=User_profile.PLAYER)
        except ObjectDoesNotExist:
            raise LogicError('No such player')
        Player.check_contact_phone(self.input['contactPhone'])
        Player.check_gender(self.input['gender'])
        Player.check_player_type(self.input['playerType'])

        player = user.player
        user.email = self.input['email']
        player.group = self.input['group']
        player.nickname = self.input['nickname']
        player.avatar_url = self.input['avatarUrl']
        player.contact_phone = self.input['contactPhone']
        player.description = self.input['description']
        player.gender = (self.input['gender'] == 'male')
        player.birthday = self.input['birthday']
        player.player_type = self.input['playerType']
        player.save()


class AdminOrganizerDetail(APIView):

    @admin_required
    def get(self):
        self.check_input('id')
        try:
            user = User.objects.get(id=self.input['id'], user_profile__user_type=User_profile.ORGANIZER)
        except ObjectDoesNotExist:
            raise LogicError('No such organizer')

        organizer = user.organizer
        return {
            'username': user.username,
            'email': user.email,
            'group': organizer.group,
            'nickname': organizer.nickname,
            'avatarUrl': organizer.avatar_url,
            'contactPhone': organizer.contact_phone,
            'description': organizer.description,
            'verifyUrl': organizer.verify_file_url,
            'verifyStatus': organizer.verify_status,
        }

    @admin_required
    def post(self):
        self.check_input('id', 'email', 'group', 'nickname', 'avatarUrl', 'description',
                         'contactPhone', 'verifyUrl')
        try:
            user = User.objects.get(id=self.input['id'], user_profile__user_type=User_profile.ORGANIZER)
        except ObjectDoesNotExist:
            raise LogicError('No such organizer')

        organizer = user.organizer
        user.email = self.input['email']
        organizer.group = self.input['group']
        organizer.nickname = self.input['nickname']
        organizer.avatar_url = self.input['avatarUrl']
        organizer.contact_phone = self.input['contactPhone']
        organizer.description = self.input['description']
        organizer.verify_file_url = self.input['verifyUrl']
        organizer.save()


class AdminOrganizerVerification(APIView):

    @admin_required
    def post(self):
        self.check_input('id', 'verify')
        try:
            user = User.objects.get(id=self.input['id'], user_profile__user_type=User_profile.ORGANIZER)
        except ObjectDoesNotExist:
            raise LogicError('No such organizer')

        organizer = user.organizer
        if self.input['verify'] == 1:
            organizer.verify_status = Organizer.VERIFIED
        else:
            organizer.verify_status = Organizer.REJECTED
        organizer.save()


class AdminContestList(APIView):

    @admin_required
    def get(self):
        contests = []
        for contest in Contest.objects.all():
            contests.append({
                'id': contest.id,
                'contestName': contest.name,
                'organizerName': contest.organizer.nickname,
                'status': contest.status
            })
        return contests


class AdminContestSearch(APIView):

    @admin_required
    def get(self):
        self.check_input('contestName', 'organizerName')
        contests = []
        for contest in Contest.objects.filter(name__contains=self.input['contestName'],
                                              organizer__nickname__contains=self.input['organizerName']):
            contests.append({
                'id': contest.id,
                'contestName': contest.name,
                'organizerName': contest.organizer.nickname,
                'status': contest.status
            })
        return contests


class AdminContestDetail(APIView):

    @admin_required
    def get(self):
        self.check_input('cid')
        contest = Contest.safe_get(id=self.input['cid'])
        return {
            'name': contest.name,
            'description': contest.description,
            'logoUrl': contest.logo_url,
            'bannerUrl': contest.banner_url,
            'signUpStartTime': time.mktime(contest.sign_up_start_time.timetuple()),
            'signUpEndTime': time.mktime(contest.sign_up_end_time.timetuple()),
            'availableSlots': contest.available_slots,
            'maxTeamMembers': contest.max_team_members,
            'signUpAttachmentUrl': contest.sign_up_attachment_url,
            'level': contest.level,
            'tags': contest.get_tags(),
            'status': contest.status
        }

    @admin_required
    def post(self):
        self.check_input('cid', 'name', 'organizerId', 'description', 'logoUrl', 'bannerUrl', 'signUpStartTime',
                         'signUpEndTime', 'availableSlots', 'maxTeamMembers', 'signUpAttachmentUrl', 'level', 'tags')
        contest = Contest.safe_get(id=self.input['cid'])

        contest.name = self.input['name']
        contest.description = self.input['description']
        contest.logo_url = self.input['logoUrl']
        contest.banner_url = self.input['bannerUrl']
        contest.sign_up_start_time = self.input['signUpStartTime']
        contest.sign_up_end_time = self.input['signUpEndTime']
        contest.available_slots = self.input['availableSlots']
        contest.max_team_members = self.input['maxTeamMembers']
        contest.sign_up_attachment_url = self.input['signUpAttachmentUrl']
        contest.level = self.input['level']
        contest.save()
        tags = self.input['tags'].split(',')
        contest.add_tags(tags)


class AdminContestVerification(APIView):

    @admin_required
    def post(self):
        self.check_input('cid', 'verify')
        contest = Contest.safe_get(id=self.input['cid'])
        if self.input['verify'] == 1:
            contest.status = Contest.PUBLISHED
        elif self.input['verify'] == 0:
            contest.status = Contest.CANCELLED
        contest.save()


class AdminAppealDetail(APIView):

    @admin_required
    def get(self):
        self.check_input('id')
        appeal = Appeal.safe_get(id=self.input['id'])
        data = {
            'contestName': appeal.target_contest.name,
            'title': appeal.title,
            'content': appeal.content,
            'attachmentUrl': appeal.attachment_url,
            'status': appeal.status,
        }

        return data

    @admin_required
    def post(self):
        self.check_input('id', 'contestId', 'title', 'content', 'attachmentUrl', 'status')
        appeal = Appeal.safe_get(id=self.input['id'])
        appeal.target_contest = Contest.safe_get(id=self.input['contestId'])
        appeal.target_organizer = appeal.target_contest.organizer
        appeal.status = self.input['status']
        appeal.title = self.input['title']
        appeal.content = self.input['content']
        appeal.attachment_url = self.input['attachmentUrl']
        appeal.save()

        return appeal.id


class AdminAppealRemove(APIView):

    @admin_required
    def post(self):
        self.check_input('id')
        appeal = Appeal.safe_get(id=self.input['id'])
        appeal.status = Appeal.REMOVED
        appeal.save()
