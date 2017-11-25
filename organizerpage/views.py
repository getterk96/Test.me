import time, pytz

from datetime import datetime

from codex.baseerror import *
from codex.baseview import APIView
from codex.basedecorator import organizer_required

from test_me_app.models import *
from test_me import settings


class Register(APIView):
    def post(self):
        # check
        self.check_input('username', 'password', 'email', 'group', 'verifyFileUrl')
        # create
        try:
            user = User.objects.create_user(username=self.input['username'],
                                            password=self.input['password'],
                                            email=self.input['email'])
            user.user_type = User_profile.ORGANIZER
            user.save()
            # default columns
            avatar_url = settings.get_url(settings.STATIC_URL + 'img/default_avatar.jpg')
            description = '请填写主办方简介'
            phone = '13000000000'
            # create organizer
            organizer = Organizer.objects.create(user=user,
                                                 nickname=self.input['username'],
                                                 group=self.input['group'],
                                                 contact_phone=phone,
                                                 avatar_url=avatar_url,
                                                 description=description,
                                                 verify_status=0,
                                                 verify_file_url=self.input['verifyFileUrl'])
            organizer.save()
        except:
            raise LogicError('Signup fail')


class PersonalInfo(APIView):
    @organizer_required
    def get(self):
        the_user = self.request.user
        organizer = the_user.organizer
        data = {
            'username': the_user.username,
            'nickname': organizer.nickname,
            'avatarUrl': organizer.avatar_url,
            'contactPhone': organizer.contact_phone,
            'email': self.request.user.email,
            'description': organizer.description,
            'verifyStatus': organizer.verify_status,
        }

        return data

    @organizer_required
    def post(self):
        self.check_input('nickname', 'avatarUrl', 'description', 'contactPhone', 'email')
        the_user = self.request.user
        organizer = the_user.organizer
        organizer.nickname = self.input['nickname']
        organizer.description = self.input['description']
        organizer.avatar_url = self.input['avatarUrl']
        organizer.contact_phone = self.input['contactPhone']
        organizer.email = self.input['email']
        organizer.save()


class OrganizingContests(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        contest = Contest.objects.get(id=self.input['id'])
        for period in contest.periods.all():
            if period.startTime < datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')):
                continue
            data = {
                'id': contest.id,
                'name': contest.name,
                'newestPeriod': period.name,
                'teamsNumber': Team.objects.filter(contest_id=contest.id).count(),
                'creatorId': contest.organizer.id,
                'creatorName': contest.organizer.name,
            }

            return data


class ContestDetail(APIView):
    @organizer_required
    def get(self):
        contest = Contest.objects.get(id=self.input['id'])
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

    @organizer_required
    def post(self):
        self.check_input('id', 'name', 'status', 'description', 'logoUrl', 'bannerUrl', 'signUpStart', 'signUpEnd',
                         'availableSlots', 'maxTeamMembers', 'signUpAttachmentUrl', 'level', 'tags')
        contest = Contest.objects.get(id=self.input['id'])
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
            tag, created = Tag.objects.get_or_create(content=content)
            tag.save()
            contest.tags.add(tag)

        contest.save()


class ContestCreate(APIView):
    @organizer_required
    def post(self):
        self.check_input('name', 'status', 'description', 'logoUrl', 'bannerUrl', 'signUpStart', 'signUpEnd',
                         'availableSlots', 'maxTeamMembers', 'signUpAttachmentUrl', 'level', 'tags')
        contest = Contest()
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
            tag, created = Tag.objects.get_or_create(content=content)
            tag.save()
            contest.tags.add(tag)

        contest.save()

        return contest.id


class ContestRemove(APIView):
    @organizer_required
    def post(self):
        self.check_input('id')
        contest = Contest.objects.get(id=self.input['id'])
        periods = Period.objects.filter(contest=contest)
        for period in periods:
            period.delete()
        contest.delete()
        return 0


class ContestBatchRemove(APIView):
    @organizer_required
    def post(self):
        self.check_input('contest_id')
        for id in self.input['contest_id']:
            contest = Contest.objects.get(id=id)
            periods = Period.objects.filter(contest=contest)
            if not periods.empty():
                for period in periods:
                    period.delete()
            contest.delete()
        return 0


class ContestTeamBatchManage(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        team = Team.objects.get(id=self.input['id'])
        scores = []
        for score in team.periodscore_set.all():
            scores.append(score.score)
        data = {
            'name': team.name,
            'leader_name': team.leader.name,
            'scores': scores,
            'status': team.status
        }

        return data

    def post(self):
        self.check_input('teamId', 'status')
        for id in self.input['teamId']:
            team = Team.objects.get(id=id)
            team.status = self.input['status']
            team.save()

        return 0


class ContestTeam(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        team = Team.objects.get(id=self.input['id'])
        data = {
            'playerNickname': team.members.values_list('nickname', flat=True),
            'playersId': team.members.values_list('id', flat=True),
            'leader': team.leader.nickname,
            'leaderId': team.leader.id,
            'avatarUrl': team.avatar_url,
            'description': team.description,
            'status': team.status,
            'signUpAttachmentUrl': team.sign_up_attachment_url,
            'periodScore': team.periodscore_set.values_list('score', flat=True),
            'questionScore': team.work_set.values_list('score', flat=True)
        }

        return data

    def post(self):
        self.check_input('id', 'status', 'periodScore', 'workScore')
        team = Team.objects.get(id=self.input['id'])
        contest = team.contest
        team.status = self.input['status']
        for index in range(len(self.input['periodScore'])):
            period_score = team.periodscore_set.get(period__index=index)
            period_score.score = self.input['periodScore'][index]
            period_score.save()
        for index in range(len(self.input['workScore'])):
            work = team.work_set.get(question__index=index)
            work.score = self.input['workScore'][index]
            work.save()
        return 0

class PeriodCreate(APIView):
    @organizer_required
    def post(self):
        self.check_input('id', 'index', 'name', 'description', 'startTime', 'endTime', 'availableSlots'
                         , 'attachmentUrl', 'questionId')
        period = Period()
        period.name = self.input['name']
        period.index = self.input['index']
        period.description = self.input['description']
        period.start_time = self.input['startTime']
        period.end_time = self.input['endTime']
        period.available_slots = self.input['availableSlots']
        period.attachment_url = self.input['attachmentUrl']
        period.contest = Contest.objects.get(id=self.input['id'])
        questions_id = self.input['questionId'].split(' ')
        period.save()
        for question_id in questions_id:
            question = ExamQuestion.objects.get(id=question_id)
            question.period = period
            question.save()

        period.save()
        return period.id


class PeriodDetail(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        period = Period.objects.get(id=self.input['id'])
        question_id = []
        for question in period.questions.all():
            question_id.append(question.id)
        data = {
            'index': period.index,
            'name': period.name,
            'description': period.description,
            'startTime': time.mktime(period.start_time.timetuple()),
            'endTime': time.mktime(period.end_time.timetuple()),
            'availableSlots': period.available_slots,
            'attachmentUrl': period.attachment_url,
            'questionId': question_id,
        }

        return data

    @organizer_required
    def post(self):
        self.check_input('id', 'index', 'name', 'description', 'startTime', 'endTime', 'availableSlots'
                         , 'attachmentUrl', 'questionId')
        # user = self.request.user
        # if user.is_authenticated:
        period = Period.objects.get(id=self.input['id'])
        period.name = self.input['name']
        period.index = self.input['index']
        period.description = self.input['description']
        period.start_time = self.input['startTime']
        period.end_time = self.input['endTime']
        period.available_slots = self.input['availableSlots']
        period.attachment_url = self.input['attachmentUrl']
        questions_id = self.input['questionId'].split(' ')
        period.save()
        for question_id in questions_id:
            question = ExamQuestion.objects.get(id=question_id)
            period.questions.add(question)

        period.save()
        return period.id


class PeriodRemove(APIView):
    @organizer_required
    def post(self):
        self.check_input('id')
        period = Period.objects.get(id=self.input['id'])
        period.delete()
        return 0


class QuestionCreate(APIView):
    @organizer_required
    def post(self):
        self.check_input('description', 'attachmentUrl', 'submissionLimit')
        # user = self.request.user
        # if user.is_authenticated:
        question = ExamQuestion()
        question.description = self.input['description']
        question.attachment_url = self.input['attachmentUrl']
        question.submission_limit = self.input['submissionLimit']
        question.save()

        question.save()
        return question.id


class QuestionDetail(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        question = ExamQuestion.objects.get(id=self.input['id'])
        data = {
            'description': question.description,
            'attachmentUrl': question.attachment_url,
            'submissionLimit': question.submission_limit,
        }

        return data

    @organizer_required
    def post(self):
        self.check_input('id', 'description', 'startTime', 'attachmentUrl', 'submissionLimit')
        # user = self.request.user
        # if user.is_authenticated:
        question = ExamQuestion.objects.get(id=self.input['id'])
        question.description = self.input['description']
        question.attachment_url = self.input['attachmentUrl']
        question.submission_limit = self.input['submissionLimit']
        question.period = Period.objects.get(id=self.input['id'])
        question.save()

        return question.id


class QuestionRemove(APIView):
    @organizer_required
    def post(self):
        self.check_input('id')
        question = ExamQuestion.objects.get(id=self.input['id'])
        question.delete()
        return 0

# Create your views here.
