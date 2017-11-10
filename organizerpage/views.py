import time

from django.core.files.storage import default_storage

from codex.baseerror import *
from codex.baseview import APIView

from test_me_app.models import Contests, Tags, Periods

from test_me.settings import SITE_DOMAIN, MEDIA_URL


class ContestDetail(APIView):
    def get(self):
        contest = Contests.objects.get(id=self.input['id'])
        tags = ""
        for tag in contest.tags.all():
            tags += tag.content
            tags += ","

        tags = tags[:-1]
        data = {
            'name': contest.name,
            'description': contest.description,
            'logoUrl': contest.logo_url,
            'bannerUrl': contest.banner_url,
            'signUpStart': time.mktime(contest.sign_up_start_time.timetuple()),
            'signUpEnd': time.mktime(contest.sign_up_end_time.timetuple()),
            'availableSlots': contest.available_slots,
            'maxTeamMembers': contest.max_team_members,
            'signUpAttachmentUrl': contest.sign_up_attachment_url,
            'level': contest.level,
            'currentTime': int(time.time()),
            'tags': tags,
        }

        return data

    def post(self):
        self.check_input('id', 'name', 'status', 'description', 'logoUrl', 'bannerUrl', 'signUpStart', 'signUpEnd', 'availableSlots'
                         , 'maxTeamMembers', 'signUpAttachmentUrl', 'level', 'tags')
        # user = self.request.user
        # if user.is_authenticated:
        contest = Contests.objects.get(id=self.input['id'])
        contest.name = self.input['name']
        contest.status = self.input['status']
        contest.description = self.input['description']
        contest.logo_url = self.input['logoUrl']
        contest.banner_url = self.input['bannerUrl']
        contest.sign_up_start_time = self.input['signUpStart']
        contest.sign_up_end_time = self.input['signUpEnd']
        contest.available_slots = self.input['availableSlots']
        contest.max_team_members = self.input['maxTeamMembers']
        contest.sign_up_attachment_url = self.input['signUpAttachmentUrl']
        contest.level = self.input['level']
        tags = self.input['tags'].split(',')
        contest.save()
        for content in tags:
            tag, created = Tags.objects.get_or_create(content=content)
            tag.save()
            contest.tags.add(tag)

        contest.save()


class ContestCreateBasic(APIView):
    def post(self):
        self.check_input('name', 'status', 'description', 'logoUrl', 'bannerUrl', 'signUpStart', 'signUpEnd', 'availableSlots'
                         , 'maxTeamMembers', 'signUpAttachmentUrl', 'level', 'tags')
        # user = self.request.user
        # if user.is_authenticated:
        contest = Contests()
        contest.name = self.input['name']
        contest.status = self.input['status']
        contest.description = self.input['description']
        contest.logo_url = self.input['logoUrl']
        contest.banner_url = self.input['bannerUrl']
        contest.sign_up_start_time = self.input['signUpStart']
        contest.sign_up_end_time = self.input['signUpEnd']
        contest.available_slots = self.input['availableSlots']
        contest.max_team_members = self.input['maxTeamMembers']
        contest.sign_up_attachment_url = self.input['signUpAttachmentUrl']
        contest.level = self.input['level']
        tags = self.input['tags'].split(',')
        contest.save()
        for content in tags:
            tag, created = Tags.objects.get_or_create(content=content)
            tag.save()
            contest.tags.add(tag)

        contest.save()

        return contest.id
        # else:
        #    raise ValidateError("请先登录")


class ContestCreateSlots(APIView):
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
        try:
            self.check_input('file')
            data = self.input['file'][0]
            path = default_storage.save(MEDIA_URL + 'file/' + data.name, data)

        except InputError:
            try:
                self.check_input('banner')
                data = self.input['banner'][0]
                path = default_storage.save(MEDIA_URL + 'img/banner/' + data.name, data)
            except InputError:
                self.check_input('logo')
                data = self.input['logo'][0]
                path = default_storage.save(MEDIA_URL + 'img/logo/' + data.name, data)

        return SITE_DOMAIN + path

# Create your views here.
