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


def player_signup_contest(player, contest):
    for team in (player.lead_teams + player.join_teams):
        if team.contest == contest:
            return team
    raise ValidateError('You have not sign up this contest')


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
            'birthday': player.birthday.strftime("%Y-%m-%d"),
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
        player.birthday = self.input['birthday']
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
        signup_flag = False
        try:
            player_signup_contest(player, contest)
        except ValidateError:
            signup_flag = True

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
            'alreadySignUp': 1 if signup_flag else 0,
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


class PlayerPeriodDetail(APIView):

    @player_required
    def get(self):
        # check
        self.check_input('pid')
        try:
            period = Period.objects.get(id=self.input['pid'])
        except ObjectDoesNotExist:
            raise InputError('Period does not exist')

        player = self.request.user.player
        team = player_signup_contest(player, period.contest)

        # get period score
        try:
            period_score = PeriodScore.objects.get(period=period, team=team)
        except ObjectDoesNotExist:
            period_score = None
        if period_score:
            score = period_score.score
            rank = period_score.rank
        else:
            score = -1
            rank = -1

        return {
            'name': period.name,
            'availableSlots': period.available_slots,
            'startTime': time.mktime(period.start_time.timetuple()),
            'endTime': time.mktime(period.end_time.timetuple()),
            'description': period.description,
            'attachmentUrl': period.attachment_url,
            'score': score,
            'rank': rank
        }


class PlayerQuestionDetail(APIView):

    @player_required
    def get(self):
        # check
        self.check_input('pid')
        try:
            period = Period.objects.get(id=self.input['pid'])
        except ObjectDoesNotExist:
            raise InputError('Period does not exist')

        player = self.request.user.player
        team = player_signup_contest(player, period.contest)

        # get question list
        questions = []
        for question in period.examquestion_set:
            try:
                work = Work.objects.get(question=question, team=team)
                submission_times = work.submission_times
                work_url = work.content_url
                score = work.score
            except ObjectDoesNotExist:
                submission_times = 0
                work_url = ''
                score = -1
            questions.append({
                'id': question.id,
                'description': question.description,
                'attachmentUrl': question.attachment_url,
                'submission_limit': question.submission_limit,
                'submission_times': submission_times,
                'workUrl': work_url,
                'score': score,
            })

        return questions


class PlayerQuestionSubmit(APIView):

    @player_required
    def post(self):
        # check input
        self.check_input('qid', 'workUrl')
        try:
            question = ExamQuestion.objects.get(id=self.input['qid'])
        except ObjectDoesNotExist:
            raise InputError('Question does not exist')

        # check signup
        player = self.request.user.player
        team = player_signup_contest(player, question.period.contest)

        # check leader
        if player != team.leader:
            raise ValidateError('Only team leader can submit work')

        try:
            work = Work.objects.get(question=question, team=team)
            work.submission_times += 1
            work.content_url = self.input['workUrl']
            work.save()
        except ObjectDoesNotExist:
            work = Work.objects.create(question=question,
                                       team=team,
                                       content_url=self.input['workUrl'])
            work.save()


class PlayerTeamList(APIView):

    @player_required
    def get(self):
        player = self.request.user.player
        teams = []
        for team in (player.lead_teams + player.join_teams):
            teams.append({
                'id': team.id,
                'name': team.name,
                'leaderName': team.leader.name,
                'contestName': team.contest.name
            })
        return teams


class PlayerTeamDetail(APIView):

    @player_required
    def get(self):
        self.check_input('tid')
        try:
            team = Team.objects.get(id=self.input['tid'])
        except ObjectDoesNotExist:
            raise InputError('Team does not exist')

        player = self.request.user.player
        if player not in (team.leader + team.members):
            raise ValidateError('You are not in this team')

        # member
        memberNames = []
        for member in team.members:
            memberNames.append(member.nickname)

        # period
        try:
            period = Period.objects.get(team=team)
            period_id = period.id
            period_name = period.name
        except ObjectDoesNotExist:
            period_id = -1
            period_name = ''

        return {
            'name': team.name,
            'leaderName': team.leader.nickname,
            'memberNames': memberNames,
            'contestId': team.contest.id,
            'contestName': team.contest.name,
            'periodId': period_id,
            'periodName': period_name,
            'avatarUrl': team.avatar_url,
            'description': team.description,
            'signUpAttachmentUrl': team.sign_up_attachment_url,
            'status': team.status
        }

    @player_required
    def post(self):
        self.check_input('tid', 'leaderId', 'memberIds', 'avatarUrl',
                         'description', 'signUpAttachmentUrl')
        try:
            team = Team.objects.get(id=self.input['tid'])
        except ObjectDoesNotExist:
            raise InputError('Team does not exist')

        player = self.request.user.player
        if team.leader != player:
            raise ValidateError('Only team leader can change team info')

        try:
            leader = User.objects.get(id=self.input['leaderId'])
            if leader.user_type != User_profile.PLAYER:
                raise InputError('Player Required')
            members = []
            for memberId in self.input['memberIds']:
                member = User.objects.get(id=memberId)
                if member.user_type != User_profile.PLAYER:
                    raise InputError('Player Required')
                members.append(member)
        except ObjectDoesNotExist:
            raise InputError('Player does not exist')

        team.leader = leader.player
        team.members.clear()
        for member in members:
            team.members.add(member.player)
        team.avatar_url = self.input['avatarUrl']
        team.description = self.input['description']
        team.sign_up_attachment_url = self.input['signUpAttachmentUrl']
        team.save()


class PlayerTeamCreate(APIView):

    @player_required
    def post(self):
        self.check_input('name', 'memberIds', 'contestId', 'avatarUrl',
                         'description', 'signUpAttachmentUrl')
        try:
            contest = Contest.objects.get(id=self.input['contestId'])
        except ObjectDoesNotExist:
            raise InputError('Contest does not exist')

        members = []
        for memberId in self.input['memberIds']:
            member = User.objects.get(id=memberId)
            if member.user_type != User_profile.PLAYER:
                raise InputError('Player does not exist')
            members.append(member)

        player = self.request.user.player
        for team in (player.lead_teams + player.join_teams):
            if team.contest == contest:
                raise LogicError('You are already in a team of this contest')

        team = Team.create(name=self.input['name'],
                           leader=player,
                           contest=contest,
                           avatar_url=self.input['avatarUrl'],
                           description=self.input['description'],
                           sign_up_attachment_url=self.input['signUpAttachmentUrl'],
                           status=Team.VERIFYING)
        for member in members:
            team.members.add(member)
        team.save()
