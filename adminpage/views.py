from codex.baseerror import *
from codex.baseview import APIView

from codex.basedecorator import admin_required
from test_me_app.models import *


class AdminUserList(APIView):

    @admin_required
    def get(self):
        user_list = []
        for user in User.objects.all():
            user_list.append({
                'id': user.id,
                'username': user.username,
                'userType': user.user_type
            })
        return user_list


class AdminUserSearch(APIView):

    @admin_required
    def get(self):
        self.check_input('username', 'userType')
        user_list = []
        for user in User.objects.filter(username__contains=self.input['username'],
                                        user_type=self.input['userType']):
            user_list.append({
                'id': user.id,
                'username': user.username,
                'userType': user.user_type
            })
        return user_list


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
            user.status = User_profile.CANCELED


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
            user.status = User_profile.NORMAL


class AdminPlayerDetail(APIView):

    @admin_required
    def get(self):
        self.check_input('id')
        try:
            user = User.objects.get(id=self.input['id'], user_type=User_profile.PLAYER)
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
            user = User.objects.get(id=self.input['id'], user_type=User_profile.PLAYER)
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
            user = User.objects.get(id=self.input['id'], user_type=User_profile.ORGANIZER)
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
                         'contactPhone', 'email', 'verifyUrl')
        try:
            user = User.objects.get(id=self.input['id'], user_type=User_profile.ORGANIZER)
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


class AdminAppealDetail(APIView):

    @admin_required
    def get(self):
        self.check_input('id')
        appeal = Appeal.safe_get(id=self.input['id'])
        data = {
            'contestName': appeal.contest.name,
            'content': appeal.content,
            'attachmentUrl': appeal.attachment_url,
            'status': appeal.status,
        }

        return data

    @admin_required
    def post(self):
        self.check_input('id', 'contestId', 'content', 'attachmentUrl', 'status')
        appeal = Appeal.safe_get(id=self.input['id'])
        appeal.target_contest = Contest.safe_get(id=self.input['contestId'])
        appeal.target_organizer = appeal.target_contest.organizer
        appeal.status = self.input['status']
        appeal.content = self.input['content']
        appeal.attachment_url = self.input['attachmentUrl']
        appeal.save()

        return appeal.id


class AdminAppealRemove(APIView):

    @admin_required
    def post(self):
        self.check_input('id')
        appeal = Appeal.safe_get(id=self.input['id'])
        try:
            appeal.delete()
        except:
            raise LogicError("Appeal Delete Failed")

        return self.input['id']
