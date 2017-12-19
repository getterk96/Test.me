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
            user.user_profile.user_type = User_profile.ORGANIZER
            user.save()
            user.user_profile.save();
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
        return {
            'username': the_user.username,
            'nickname': organizer.nickname,
            'avatarUrl': organizer.avatar_url,
            'contactPhone': organizer.contact_phone,
            'email': self.request.user.email,
            'description': organizer.description,
            'verifyStatus': organizer.verify_status,
        }

    @organizer_required
    def post(self):
        self.check_input('nickname', 'avatarUrl', 'description', 'contactPhone', 'email')
        organizer = self.request.user.organizer
        organizer.nickname = self.input['nickname']
        organizer.description = self.input['description']
        organizer.avatar_url = self.input['avatarUrl']
        organizer.contact_phone = self.input['contactPhone']
        organizer.email = self.input['email']
        organizer.save()


class OrganizingContests(APIView):
    @organizer_required
    def get(self):
        contests = Contest.objects.filter(organizer_id=self.request.user.organizer.id)
        organizing_contests = []
        for contest in contests:
            organizing_contests.append({
                'id': contest.id,
                'name': contest.name,
                'teamsNumber': Team.objects.filter(contest_id=contest.id).count(),
                'creatorId': contest.organizer.id,
                'creatorName': contest.organizer.nickname,
            })
        return organizing_contests


class ContestDetail(APIView):
    @organizer_required
    def get(self):
        contest = Contest.safe_get(id=self.input['id'])
        return {
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
            'tags': contest.get_tags(),
            'periods': list(contest.period_set.values_list('id', flat=True))
        }

    @organizer_required
    def post(self):
        self.check_input('id', 'name', 'description', 'logoUrl', 'bannerUrl', 'signUpStart', 'signUpEnd',
                         'availableSlots', 'maxTeamMembers', 'signUpAttachmentUrl', 'level', 'tags')
        contest = Contest.safe_get(id=self.input['id'])
        contest.name = self.input['name']
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
        contest.add_tags(tags)
        contest.save()


class ContestCreate(APIView):
    @organizer_required
    def post(self):
        self.check_input('name', 'description', 'logoUrl', 'bannerUrl', 'signUpStart', 'signUpEnd',
                         'availableSlots', 'maxTeamMembers', 'signUpAttachmentUrl', 'level', 'tags')
        contest = Contest()
        contest.name = self.input['name']
        contest.description = self.input['description']
        contest.logo_url = self.input['logoUrl']
        contest.banner_url = self.input['bannerUrl']
        contest.sign_up_start_time = self.input['signUpStart']
        contest.sign_up_end_time = self.input['signUpEnd']
        contest.available_slots = self.input['availableSlots']
        contest.max_team_members = self.input['maxTeamMembers']
        contest.sign_up_attachment_url = self.input['signUpAttachmentUrl']
        contest.level = self.input['level']
        contest.organizer_id = self.request.user.organizer.id
        contest.status = Contest.SAVED
        contest.save()
        tags = self.input['tags'].split(',')
        contest.add_tags(tags)

        return contest.id


class ContestRemove(APIView):
    @organizer_required
    def post(self):
        self.check_input('id')
        contest = Contest.safe_get(id=self.input['id'])
        periods = Period.objects.filter(contest=contest)
        if not periods.empty:
            for period in periods:
                period.delete()
        contest.delete()


class ContestBatchRemove(APIView):
    @organizer_required
    def post(self):
        self.check_input('contest_id')
        for id in self.input['contest_id']:
            contest = Contest.safe_get(id=id)
            periods = Period.objects.filter(contest=contest)
            if not periods.empty():
                for period in periods:
                    period.delete()
            contest.delete()


class ContestTeamBatchManage(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        team = Team.safe_get(id=self.input['id'])
        scores = []
        for score in team.periodscore_set.all():
            scores.append(score.score)
        return {
            'id': team.id,
            'name': team.name,
            'leader_name': team.leader.name,
            'scores': scores,
            'status': team.status
        }

    @organizer_required
    def post(self):
        self.check_input('teamId', 'status')
        for id in self.input['teamId']:
            team = Team.safe_get(id=id)
            team.status = self.input['status']
            team.save()


class ContestTeamDetail(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        team = Team.safe_get(id=self.input['id'])

        # members
        members = []
        for member in team.members:
            members.append({
                'id': member.id,
                'name': member.user.username
            })

        # period
        periods = []
        if team.period:
            current_period_id = team.period.id
            current_period_name = team.period.name
            for period in team.contest.period_set.all():
                # period score
                try:
                    period_score = PeriodScore.objects.get(period=period, team=team)
                    score = period_score.score
                    rank = period_score.rank
                except ObjectDoesNotExist:
                    score = -1
                    rank = -1
                # period works
                works = []
                for question in period.examquestion_set.all():
                    try:
                        work = Work.objects.get(question=question, team=team)
                        work_content_url = work.content_url
                        work_score = work.score
                        work_submission_times = work.submission_times
                    except ObjectDoesNotExist:
                        work_content_url = ''
                        work_score = -1
                        work_submission_times = -1
                    works.append({
                        'questionId': question,
                        'questionIndex': question.index,
                        'questionDescription': question.description,
                        'workContentUrl': work_content_url,
                        'workScore': work_score,
                        'workSubmissionTimes': work_submission_times
                    })
                periods.append({
                    'id': period.id,
                    'name': period.name,
                    'index': period.index,
                    'score': score,
                    'rank': rank,
                    'works': works
                })

        else:
            current_period_id = -1
            current_period_name = ''

        return {
            'name': team.name,
            'leader': {'id': team.leader.id, 'name': team.leader.user.username},
            'members': members,
            'periodId': current_period_id,
            'periodName': current_period_name,
            'avatarUrl': team.avatar_url,
            'description': team.description,
            'status': team.status,
            'signUpAttachmentUrl': team.sign_up_attachment_url,
            'periods': periods
        }

    @organizer_required
    def post(self):
        self.check_input('tid', 'name', 'leaderId', 'memberIds', 'avatarUrl', 'description', 'signUpAttachmentUrl',
                         'periodId''status', 'periods')
        team = Team.safe_get(id=self.input['id'])

        # basic info
        team.name = self.input['name']
        team.avatar_url = self.input['avatarUrl'],
        team.description = self.input['signUpAttachmentUrl']
        team.status = self.input['status']
        try:
            # leader
            leader = User.objects.get(id=self.input['leaderId'])
            if leader.user_type != User_profile.PLAYER:
                raise InputError('Player Required')
            team.leader = leader
            # members
            team.members.clear()
            for memberId in self.input['memberIds']:
                member = User.objects.get(id=memberId)
                if member.user_type != User_profile.PLAYER:
                    raise InputError('Player Required')
                team.members.add(member)
        except ObjectDoesNotExist:
            raise InputError('Player does not exist')
        # current period
        period = Period.safe_get(id=input['periodId'])
        team.period = period
        team.save()

        # work and score
        for period_info in self.input['periods']:
            period = Period.safe_get(id=period_info['id'])
            # period score
            try:
                period_score = PeriodScore.safe_get(period=period, team=team)
                period_score.score = period_info['score']
                period_score.rank = period_info['rank']
                period_score.save()
            except LogicError:
                PeriodScore.objects.create(period=period, team=team,
                                   score=period_info['score'],
                                   rank=period_info['rank'])
            # work
            works = period_info['work']
            for work in works:
                question = ExamQuestion.safe_get(id=work['questionId'])
                try:
                    work = Work.safe_get(question=question, team=team)
                    work.content_url = work['workContentUrl']
                    work.score = work['workScore']
                    work.submission_times = work['submission_times']
                    work.save()
                except LogicError:
                    Work.objects.create(question=question, team=team,
                                        content_url=work['workContentUrl'],
                                        score=work['workScore'],
                                        submission_times=work['submission_times'])


class PeriodCreate(APIView):
    @organizer_required
    def post(self):
        self.check_input('id', 'index', 'name', 'description', 'startTime', 'endTime', 'availableSlots'
                         , 'attachmentUrl')
        period = Period()
        period.name = self.input['name']
        period.index = self.input['index']
        period.description = self.input['description']
        period.start_time = self.input['startTime']
        period.end_time = self.input['endTime']
        period.available_slots = self.input['availableSlots']
        period.attachment_url = self.input['attachmentUrl']
        period.contest = Contest.safe_get(id=self.input['id'])
        period.save()

        return period.id


class PeriodDetail(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        period = Period.safe_get(id=self.input['id'])
        question_id = []
        for question in ExamQuestion.objects.filter(period_id=self.input['id']):
            question_id.append(question.id)
        return {
            'index': period.index,
            'name': period.name,
            'description': period.description,
            'startTime': time.mktime(period.start_time.timetuple()),
            'endTime': time.mktime(period.end_time.timetuple()),
            'availableSlots': period.available_slots,
            'attachmentUrl': period.attachment_url,
            'questionId': question_id,
        }

    @organizer_required
    def post(self):
        self.check_input('id', 'index', 'name', 'description', 'startTime', 'endTime', 'availableSlots',
                         'attachmentUrl', 'questionId')
        period = Period.safe_get(id=self.input['id'])
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
            question = ExamQuestion.safe_get(id=question_id)
            period.examquestion_set.add(question)
            period.save()

        return period.id


class PeriodRemove(APIView):
    @organizer_required
    def post(self):
        self.check_input('id')
        period = Period.safe_get(id=self.input['id'])
        period.delete()


class QuestionCreate(APIView):
    @organizer_required
    def post(self):
        self.check_input('periodId', 'description', 'attachmentUrl', 'submissionLimit', 'index')
        question = ExamQuestion()
        question.description = self.input['description']
        question.attachment_url = self.input['attachmentUrl']
        question.submission_limit = self.input['submissionLimit']
        question.period_id = self.input['periodId']
        question.index = self.input['index']
        question.save()

        return question.id


class QuestionDetail(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        question = ExamQuestion.safe_get(id=self.input['id'])
        return {
            'description': question.description,
            'attachmentUrl': question.attachment_url,
            'submissionLimit': question.submission_limit,
        }

    @organizer_required
    def post(self):
        self.check_input('id', 'periodId', 'description', 'startTime', 'attachmentUrl', 'submissionLimit')
        question = ExamQuestion.safe_get(id=self.input['id'])
        question.description = self.input['description']
        question.attachment_url = self.input['attachmentUrl']
        question.submission_limit = self.input['submissionLimit']
        question.period = Period.safe_get(id=self.input['periodId'])
        question.save()

        return question.id


class QuestionRemove(APIView):
    @organizer_required
    def post(self):
        self.check_input('id')
        question = ExamQuestion.safe_get(id=self.input['id'])
        question.delete()


class AppealList(APIView):
    @organizer_required
    def get(self):
        pass


class AppealDetail(APIView):
    @organizer_required
    def get(self):
        self.check_input('id')
        appeal = Appeal.safe_get(id=self.input['id'])
        return {
            'contestName': appeal.contest.name,
            'content': appeal.content,
            'attachmentUrl': appeal.attachment_url,
            'status': appeal.status,
        }

    @organizer_required
    def post(self):
        self.check_input('id', 'status')
        appeal = Appeal.safe_get(id=self.input['id'])
        appeal.status = self.input['status']
        appeal.save()

        return appeal.id
