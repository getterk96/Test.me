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
