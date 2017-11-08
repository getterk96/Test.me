from codex.baseerror import *
from codex.baseview import APIView

from test_me_app.models import Contests, Tags, Periods

from test_me.settings import SITE_DOMAIN

class ContestDetail(APIView):
    def get(self):
        self.check_input('id')
        user = self.request.user
        if user.is_authenticated:
            contest = Contests.objects.get(id=self.input['id'])
            data = {
                'name': contest.name,
                'description': contest.description,
                'logoUrl': contest.logo_url,
                'bannerUrl': contest.banner_url,
                'signUpStart': time.mktime(contest.sign_up_start_time.timetuple()),
                'signUpEnd': time.mktime(contest.sign_up_start_time.timetuple()),
                'availableSlots': contest.available_slots,
                'maxTeamMembers': contest.max_team_members,
                'signUpAttachmentUrl': contest.sign_up_attachment_url,
                'level': contest.level,
                'currentTime': int(time.time()),
                'tags': Tags.objects.filter(contest_with_tag=contest),
                'periods': Periods.objects.filter(contest=contest),
            }
            return data

        else:
            raise ValidateError("请先登录")

    def post(self):
        self.check_input('name', 'place', 'description', 'picUrl', 'startTime', 'endTime', 'bookStart', 'bookEnd'
                         , 'status', 'totalTickets')
        user = self.request.user
        if user.is_authenticated:
            contest = Contests.objects.get(id=self.input['id'])
            contest.name = self.input['name']
            contest.description = self.input['description']
            contest.log_url = self.input['logoUrl']
            contest.banner_url = self.input['bannerUrl']
            contest.sign_up_start_time = self.input['signUpStart']
            contest.sign_up_end_time = self.input['signUpEnd']
            contest.available_slots = self.input['availableSlots']
            contest.max_team_members = self.input['maxTeamMembers']
            contest.sign_up_attachment_url = self.input['signUpAttachmentUrl']
            contest.level = self.input['level']
            contest.save()

        else:
            raise ValidateError("请先登录")


class ContestCreateBasic(APIView):
    def post(self):
        self.check_input('image')
        user = self.request.user
        if user.is_authenticated:
            data = self.input['image'][0]
            path = default_storage.save('img/' + data.name, data)
            return SITE_DOMAIN + '/media/' + path

        else:
            raise ValidateError("请先登录")


class ContestCreateStage(APIView):
    def post(self):
        self.check_input('image')
        user = self.request.user
        if user.is_authenticated:
            data = self.input['image'][0]
            path = default_storage.save('img/' + data.name, data)
            return SITE_DOMAIN + '/media/' + path

        else:
            raise ValidateError("请先登录")


class ContestUpload(APIView):
    def post(self):
        self.check_input('image')
        user = self.request.user
        if user.is_authenticated:
            data = self.input['image'][0]
            path = default_storage.save('img/' + data.name, data)
            return SITE_DOMAIN + '/media/' + path

        else:
            raise ValidateError("请先登录")

# Create your views here.
