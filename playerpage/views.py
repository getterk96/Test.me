from itertools import chain
from codex.baseerror import *
from codex.baseview import APIView
from codex.basedecorator import *
from test_me_app.models import *
from test_me import settings
import time, datetime


def player_signup_contest(player, contest):
    for team in player.lead_teams.all():
        if team.contest == contest:
            return team
    for invitation in TeamInvitation.objects.filter(player=player, team__contest=contest):
        if invitation.status == TeamInvitation.CONFIRMED:
            return invitation.team
    raise LogicError('You have not sign up this contest')


class PlayerRegister(APIView):

    def post(self):
        # check
        self.check_input('username', 'password', 'email', 'group', 'gender', 'playerType', 'birthday')
        Player.check_gender(self.input['gender'])
        Player.check_player_type(self.input['playerType'])
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
        Player.check_contact_phone(self.input['contactPhone'])
        Player.check_gender(self.input['gender'])
        Player.check_player_type(self.input['playerType'])
        # change
        player = self.request.user.player
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
        self.request.user.save()


class PlayerParticipatingContests(APIView):

    @player_required
    def get(self):
        player = self.request.user.player
        contests = []
        for team in chain(player.lead_teams.exclude(status=Team.DISMISSED),
                          player.join_teams.exclude(status=Team.DISMISSED)):
            contests.append({'id': team.contest.id,
                             'name': team.contest.name,
                             'organizerName': team.contest.organizer.nickname,
                             'logoUrl':team.contest.logo_url})
        return contests


class PlayerContestDetail(APIView):

    @player_required
    def get(self):
        # check
        self.check_input('cid')
        contest = Contest.safe_get(id=self.input['cid'])

        # already sign up
        player = self.request.user.player
        signup_flag = True
        try:
            player_signup_contest(player, contest)
        except LogicError:
            signup_flag = False

        # tags
        tags = []
        for tag in contest.tags.all():
            tags.append(tag.content)
        # periods
        periods = []
        for period in contest.period_set.exclude(status=Period.REMOVED):
            periods.append({'periodName': period.name,
                            'periodId': period.id,
                            'periodSlots': period.available_slots,
                            'periodStartTime': time.mktime(period.start_time.timetuple()),
                            'periodEndTime': time.mktime(period.end_time.timetuple())})

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


class PlayerContestSearchSimple(APIView):

    @player_required
    def get(self):
        # check
        self.check_input('keyword')

        # search
        results = Contest.objects.filter(name__contains=self.input['keyword'])
        # return
        contests = []
        for result in results:
            contests.append({
                'id': result.id,
                'name': result.name,
                'logoUrl': result.logo_url,
                'organizerName': result.organizer.nickname,
                'level': result.level,
                'signUpStartTime': time.mktime(result.sign_up_start_time.timetuple()),
                'signUpEndTime': time.mktime(result.sign_up_end_time.timetuple()),
            })
        return contests


class PlayerPeriodDetail(APIView):

    @player_required
    def get(self):
        # check
        period = Period.safe_get(id=self.input['pid'])

        player = self.request.user.player
        team = player_signup_contest(player, period.contest)

        # get period score
        try:
            period_score = PeriodScore.objects.get(period=period, team=team)
            score = period_score.score
            rank = period_score.rank
        except ObjectDoesNotExist:
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
        period = Period.safe_get(id=self.input['pid'])

        player = self.request.user.player
        team = player_signup_contest(player, period.contest)

        # get question list
        questions = []
        for question in period.examquestion_set.exclude(status=ExamQuestion.REMOVED):
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
        question = ExamQuestion.safe_get(id=self.input['qid'])

        # check signup
        player = self.request.user.player
        team = player_signup_contest(player, question.period.contest)

        # check in this period
        if not team.period or team.period != question.period or team.status != Team.VERIFIED:
            raise LogicError('You can not submit for this question')

        # check period time
        if team.period.start_time.timetuple() > datetime.datetime.now().timetuple() or \
           team.period.end_time.timetuple() < datetime.datetime.now().timetuple():
            raise LogicError('Can not submit now')

        # check leader
        if player != team.leader:
            raise LogicError('Only team leader can submit work')

        try:
            work = Work.objects.get(question=question, team=team)
            if work.submission_times >= question.submission_limit:
                raise LogicError('Out of submission limit')
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
        for team in chain(player.lead_teams.exclude(status=Team.DISMISSED),
                          player.join_teams.exclude(status=Team.DISMISSED)):
            if team.status == Team.VERIFYING or team.status == Team.VERIFIED or team.status == Team.CREATING:
                teams.append({
                    'id': team.id,
                    'name': team.name,
                    'leaderName': team.leader.nickname,
                    'contestName': team.contest.name,
                    'cid' : team.contest.id
                })
        return teams


class PlayerTeamCreate(APIView):

    @player_required
    def post(self):
        self.check_input('name', 'members', 'contestId', 'avatarUrl',
                         'description', 'signUpAttachmentUrl')
        contest = Contest.safe_get(id=self.input['contestId'])

        # check signup time
        if contest.sign_up_start_time.timetuple() > datetime.datetime.now().timetuple() or \
           contest.sign_up_end_time.timetuple() < datetime.datetime.now().timetuple():
            raise LogicError('Contest is not in sign up time')

        # check already sign up
        player = self.request.user.player
        team = None
        try:
            team = player_signup_contest(player, contest)
        except LogicError:
            pass
        if team:
            raise LogicError('You are already in a team of this contest')

        # check members
        members = []
        for memberName in self.input['members']:
            try:
                member = User.objects.get(username=memberName, user_profile__user_type=User_profile.PLAYER)
            except ObjectDoesNotExist:
                raise InputError('Player does not exist')
            team = None
            try:
                player_signup_contest(member.player, contest)
            except LogicError:
                pass
            if team:
                raise LogicError('Member ' + member.user.username + ' is already in a team of this contest')
            members.append(member)

        # check team number
        if len(members) + 1 > contest.max_team_members:
            raise LogicError('Number of team member should be no more than ' + str(contest.max_team_members))

        # check total team number
        if contest.team_set.filter(status__in=[Team.VERIFYING, Team.VERIFIED]).count() + 1 > contest.available_slots:
            raise LogicError('No more team could sign up, max team number: ' + str(contest.available_slots))

        # create team and invitations
        team = Team.objects.create(name=self.input['name'],
                                   leader=player,
                                   contest=contest,
                                   avatar_url=self.input['avatarUrl'],
                                   description=self.input['description'],
                                   sign_up_attachment_url=self.input['signUpAttachmentUrl'],
                                   status=Team.CREATING)
        for member in members:
            team.members.add(member.player)
            TeamInvitation.objects.create(team=team, player=member.player)
        team.save()


class PlayerTeamDetail(APIView):

    @player_required
    def get(self):
        self.check_input('tid')
        team = Team.safe_get(id=self.input['tid'])
        player = self.request.user.player
        if player != team.leader and player not in team.members.all():
            raise ValidateError('You are not in this team')

        # member
        members = []
        for member in team.members.all():
            invitation = TeamInvitation.safe_get(player=member, team=team)
            members.append({
                'id': member.user.id,
                'name': member.user.username,
                'nickname': member.nickname,
                'invitationStatus': invitation.status,
                'avatarUrl': member.avatar_url,
                'group': member.group
            })

        # period
        if team.period:
            period_id = team.period.id
            period_name = team.period.name
        else:
            period_id = -1
            period_name = ''

        return {
            'name': team.name,
            'leader': {'id': team.leader.user.id,
                'name': team.leader.user.username,
                'nickname': team.leader.nickname,
                'avatarUrl': team.leader.avatar_url,
                'group': team.leader.group
            },
            'members': members,
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
        team = Team.safe_get(id=self.input['tid'])

        # check leader
        player = self.request.user.player
        if team.leader != player:
            raise ValidateError('Only team leader can change team info')

        # check team status
        if team.status != Team.CREATING:
            raise LogicError('Can not modify signed-up team info')

        # check number of team member
        if len(self.input['memberIds']) + 1 > team.contest.max_team_members:
            raise LogicError('Number of team member should be no more than ' + str(team.contest.max_team_members))

        # Modify team info
        try:
            # check leader
            new_leader = User.objects.get(id=self.input['leaderId'], user_profile__user_type=User_profile.PLAYER)
            leader_team = None
            try:
                leader_team = player_signup_contest(new_leader.player, team.contest)
            except LogicError:
                pass
            if leader_team and leader_team != team:
                raise LogicError('Leader ' + new_leader.username + 'is already in another team of this contest')
            # check members
            new_members = []
            for memberId in self.input['memberIds']:
                member = User.objects.get(id=memberId, user_profile__user_type=User_profile.PLAYER)
                member_team = None
                try:
                    member_team = player_signup_contest(member.player, team.contest)
                except LogicError:
                    pass
                if member_team and member_team != team:
                    raise LogicError('Member ' + member.username + ' is already in another team of this contest')
                new_members.append(member.player)
        except ObjectDoesNotExist:
            raise InputError('Player does not exist')

        team.leader = new_leader.player

        # delete old members with invitations
        for member in team.members.all():
            if member not in new_members:
                print('1 ', member.user.id)
                invitation = TeamInvitation.safe_get(team=team, player=member)
                invitation.status = TeamInvitation.REMOVED
                invitation.save()
        team.members.clear()

        # add new members
        for member in new_members:
            team.members.add(member)
            try:
                print('2 ', member.id)
                TeamInvitation.safe_get(team=team, player=member)
            except LogicError:
                print('3 ', member.id)
                TeamInvitation.objects.create(team=team, player=member)

        # other info
        team.avatar_url = self.input['avatarUrl']
        team.description = self.input['description']
        team.sign_up_attachment_url = self.input['signUpAttachmentUrl']
        team.save()


class PlayerTeamDismiss(APIView):

    @player_required
    def post(self):
        self.check_input('tid')
        team = Team.safe_get(id=self.input['tid'])
        player = self.request.user.player
        if player != team.leader:
            raise ValidateError('Only team leader can dismiss team')

        team.status = Team.DISMISSED
        for invitation in team.teaminvitation_set.all():
            invitation.status = TeamInvitation.REMOVED
            invitation.save()
        team.save()


class PlayerTeamInvitation(APIView):

    @player_required
    def get(self):
        invitations = []
        for invitation in self.request.user.player.teaminvitation_set.exclude(status=TeamInvitation.REMOVED):
            member_ids = []
            member_names = []
            for member in invitation.team.members.all():
                member_ids.append(member.id)
                member_names.append(member.user.username)
            invitations.append({
                'id': invitation.id,
                'contestId': invitation.team.contest.id,
                'leaderId': invitation.team.leader.id,
                'leaderName': invitation.team.leader.user.username,
                'memberIds': member_ids,
                'memberNames': member_names,
                'teamName': invitation.team.name,
            })
        return invitations

    @player_required
    def post(self):
        self.check_input('iid', 'confirm')
        invitation = TeamInvitation.safe_get(id=self.input['iid'], status=TeamInvitation.CONFIRMING)
        if self.input['confirm'] == 1:
            invitation.status = TeamInvitation.CONFIRMED
        elif self.input['confirm'] == 0:
            invitation.status = TeamInvitation.REFUSED
        invitation.save()
        

class PlayerTeamSignUp(APIView):

    @player_required
    def post(self):
        self.check_input('tid')
        team = Team.safe_get(id=self.input['tid'])

        if team.contest.sign_up_start_time.timetuple() > datetime.datetime.now().timetuple() or \
           team.contest.sign_up_end_time.timetuple() < datetime.datetime.now().timetuple():
            raise LogicError('Contest is not in sign up time')

        player = self.request.user.player
        if player != team.leader:
            raise LogicError('Only team leader can sign up for team')
        for invitation in team.teaminvitation_set.all():
            if invitation.status != TeamInvitation.CONFIRMED and invitation.status != TeamInvitation.REMOVED:
                raise LogicError('Team can sign up until all members confirm')
        team.status = Team.VERIFYING
        team.save()


class PlayerAppealCreate(APIView):

    @player_required
    def post(self):
        self.check_input('contestId', 'title', 'content', 'attachmentUrl', 'type')
        contest = Contest.safe_get(id=self.input['contestId'])
        initiator_team = Team.safe_get(contest=contest, leader=self.request.user.player)
        appeal = Appeal.objects.create(initiator=initiator_team,
                                       target_contest=contest,
                                       title=self.input['title'],
                                       content=self.input['content'],
                                       attachment_url=self.input['attachmentUrl'],
                                       status=Appeal.TOSOLVE,
                                       type=self.input['type'])
        return appeal.id


class PlayerAppealList(APIView):

    @player_required
    def get(self):
        self.check_input('cid', 'tid')
        contest = Contest.safe_get(id=self.input['cid'])
        team = Team.safe_get(id=self.input['tid'])
        appeals = []
        for appeal in Appeal.objects.exclude(status=Appeal.REMOVED).\
                filter(target_contest=contest, initiator=team):
            appeals.append({
                'id': appeal.id,
                'title': appeal.title,
                'status': appeal.status
            })
        return appeals


class PlayerAppealDetail(APIView):

    @player_required
    def get(self):
        self.check_input('id')
        appeal = Appeal.safe_get(id=self.input['id'])
        return {
            'contestName': appeal.target_contest.name,
            'title': appeal.title,
            'content': appeal.content,
            'attachmentUrl': appeal.attachment_url,
            'status': appeal.status,
        }

    @player_required
    def post(self):
        self.check_input('id', 'contestId', 'title', 'content', 'attachmentUrl', 'status')
        appeal = Appeal.safe_get(id=self.input['id'])
        appeal.target_contest = Contest.safe_get(id=self.input['contestId'])
        appeal.status = self.input['status']
        appeal.title = self.input['title']
        appeal.content = self.input['content']
        appeal.attachment_url = self.input['attachmentUrl']
        appeal.save()

        return appeal.id


class PlayerAppealRemove(APIView):

    @player_required
    def post(self):
        self.check_input('id')
        appeal = Appeal.safe_get(id=self.input['id'])
        appeal.status = Appeal.REMOVED
        appeal.save()


class PlayerSearch(APIView):

    @player_required
    def get(self):
        self.check_input('username')
        try:
            user = User.objects.get(username=self.input['username'], user_profile__user_type=User_profile.PLAYER)
            return {'id': user.id}
        except ObjectDoesNotExist:
            return {'id': -1}
