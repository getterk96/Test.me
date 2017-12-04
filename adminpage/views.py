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
