from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from codex.baseerror import *
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.

class User_profile(models.Model):
    user = models.OneToOneField(User)
    user_type = models.IntegerField(default=0)
    PLAYER = 0
    ORGANIZER = 1
    ADMINISTRATOR = 2

    status = models.IntegerField(default=0)
    NORMAL = 0
    CANCELED = 1


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = User_profile()
        profile.user = instance
        profile.save()


post_save.connect(create_user_profile, sender=User)


class UserCommon(models.Model):
    group = models.CharField(max_length=128)
    # for players, group may mean their university or so
    # for organizers, group may mean their corporation or university or so
    nickname = models.CharField(max_length=20)
    avatar_url = models.CharField(max_length=256)
    contact_phone = models.CharField(max_length=20, default="")
    description = models.TextField()

    class Meta:
        abstract = True


class Player(UserCommon):
    user = models.OneToOneField(User, related_name='player')
    gender = models.BooleanField()
    birthday = models.DateField()
    player_type = models.IntegerField()

    UNDERGRADUATE = 0
    POSTGRADUATE = 1
    JUNIOR_COLLEGE_STUDENT = 2
    HIGH_SCHOOL_STUDENT = 3
    OUTSIDER = 4

    @staticmethod
    def check_gender(gender):
        if gender not in ['male', 'female']:
            raise InputError('Wrong gender')

    @staticmethod
    def check_player_type(player_type):
        if player_type < 0 or player_type > 4:
            raise InputError('Wrong player type')

    @staticmethod
    def check_contact_phone(contact_phone):
        for c in contact_phone:
            if c < '0' or c > '9':
                raise InputError('Wrong contact phone')


class Organizer(UserCommon):
    user = models.OneToOneField(User, related_name='organizer')
    verify_file_url = models.CharField(max_length=256)

    verify_status = models.IntegerField()
    VERIFYING = 0
    VERIFIED = 1
    REJECTED = -1


class Tag(models.Model):
    content = models.CharField(max_length=20)


class Contest(models.Model):
    name = models.CharField(max_length=64)
    organizer = models.ForeignKey(Organizer)
    description = models.TextField()
    logo_url = models.CharField(max_length=256)
    banner_url = models.CharField(max_length=256)
    sign_up_start_time = models.DateTimeField()
    sign_up_end_time = models.DateTimeField()
    available_slots = models.IntegerField()
    max_team_members = models.IntegerField()
    sign_up_attachment_url = models.CharField(max_length=256)
    tags = models.ManyToManyField(Tag)

    level = models.IntegerField()
    INTERNATIONAL = 0
    NATIONAL = 1
    PROVINCIAL = 2
    MUNICIPAL = 3
    DISTRICT = 4
    SCHOOL = 5
    DEPARTMENT = 6

    status = models.IntegerField()
    CANCELLED = -1
    SAVED = 0
    VERIFYING = 1
    PUBLISHED = 2

    @staticmethod
    def safe_get(**kwargs):
        try:
            return Contest.objects.get(**kwargs)
        except ObjectDoesNotExist:
            raise LogicError("No Such Contest")

    def add_tags(self, tags):
        for content in tags:
            if not content:
                continue
            tag, created = Tag.objects.get_or_create(content=content)
            if not created:
                self.save()
                raise LogicError("Tag Create Error")
            tag.save()
            self.tags.add(tag)

        self.save()

    def get_tags(self):
        tags = ""
        for tag in self.tags.all():
            tags += tag.content
            tags += ","
        return tags


class Period(models.Model):
    contest = models.ForeignKey(Contest)
    index = models.IntegerField()
    name = models.CharField(max_length=20)
    available_slots = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()
    attachment_url = models.CharField(max_length=256)

    status = models.IntegerField(default=1)
    NORMAL = 1
    REMOVED = -1

    @staticmethod
    def safe_get(**kwargs):
        try:
            return Period.objects.exclude(status=Period.REMOVED).get(**kwargs)
        except ObjectDoesNotExist:
            raise LogicError("No Such Period")


class ExamQuestion(models.Model):
    period = models.ForeignKey(Period)
    index = models.IntegerField()
    description = models.TextField()
    attachment_url = models.CharField(max_length=256)
    submission_limit = models.IntegerField()

    status = models.IntegerField(default=1)
    NORMAL = 1
    REMOVED = -1

    @staticmethod
    def safe_get(**kwargs):
        try:
            return ExamQuestion.objects.exclude(status=ExamQuestion.REMOVED).get(**kwargs)
        except ObjectDoesNotExist:
            raise LogicError("No Such Exam Question")


class Team(models.Model):
    name = models.CharField(max_length=20)
    leader = models.ForeignKey(Player, related_name="lead_teams")
    members = models.ManyToManyField(Player, related_name="join_teams")
    contest = models.ForeignKey(Contest)
    period = models.ForeignKey(Period, null=True)
    avatar_url = models.CharField(max_length=256)
    description = models.TextField()
    sign_up_attachment_url = models.CharField(max_length=256)

    status = models.IntegerField()
    CREATING = 0
    VERIFYING = 1
    VERIFIED = 2
    DISMISSED = -1

    @staticmethod
    def safe_get(**kwargs):
        try:
            return Team.objects.exclude(status=Team.DISMISSED).get(**kwargs)
        except ObjectDoesNotExist:
            raise LogicError("No Such Team")


class TeamInvitation(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)

    status = models.IntegerField(default=0)
    CONFIRMING = 0
    CONFIRMED = 1
    REFUSED = 2
    REMOVED = -1

    @staticmethod
    def safe_get(**kwargs):
        try:
            return TeamInvitation.objects.exclude(status=TeamInvitation.REMOVED).get(**kwargs)
        except ObjectDoesNotExist:
            raise LogicError('No such team invitation')


class PeriodScore(models.Model):
    period = models.ForeignKey(Period)
    team = models.ForeignKey(Team)
    score = models.IntegerField()
    rank = models.IntegerField()

    @staticmethod
    def safe_get(**kwargs):
        try:
            return TeamInvitation.objects.get(**kwargs)
        except ObjectDoesNotExist:
            raise LogicError('No such period score')


class Work(models.Model):
    question = models.ForeignKey(ExamQuestion)
    team = models.ForeignKey(Team)
    content_url = models.CharField(max_length=256)
    score = models.IntegerField(default=-1)
    submission_times = models.IntegerField(default=1)

    @staticmethod
    def safe_get(**kwargs):
        try:
            return TeamInvitation.objects.get(**kwargs)
        except ObjectDoesNotExist:
            raise LogicError('No such work')


class Appeal(models.Model):
    initiator = models.ForeignKey(Player)
    target_contest = models.ForeignKey(Contest)
    title = models.CharField(max_length=256)
    content = models.TextField()
    attachment_url = models.CharField(max_length=256)

    status = models.IntegerField()
    TOSOLVE = 0
    SOLVED = 1
    ACCEPTED = 2
    REMOVED = -1

    @staticmethod
    def safe_get(**kwargs):
        try:
            return Appeal.objects.exclude(status=Appeal.REMOVED).get(**kwargs)
        except ObjectDoesNotExist:
            raise LogicError("No Such Appeal")
