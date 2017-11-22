from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save


# Create your models here.

class User_profile(models.Model):
    user = models.OneToOneField(User)
    user_type = models.IntegerField(default=0)
    PLAYER = 0
    ORGANIZER = 1
    ADMINISTRATOR = 2


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
    PUBLISHED = 1


class Period(models.Model):
    contest = models.ForeignKey(Contest)
    index = models.IntegerField()
    name = models.CharField(max_length=20)
    available_slots = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()
    attachment_url = models.CharField(max_length=256)


class ExamQuestion(models.Model):
    period = models.ForeignKey(Period)
    index = models.IntegerField()
    description = models.TextField()
    attachment_url = models.CharField(max_length=256)
    submission_limit = models.IntegerField()


class Team(models.Model):
    name = models.CharField(max_length=20)
    leader = models.ForeignKey(Player, related_name="lead_teams")
    members = models.ManyToManyField(Player, related_name="join_teams")
    contest = models.ForeignKey(Contest)
    period = models.ForeignKey(Period)
    avatar_url = models.CharField(max_length=256)
    description = models.TextField()
    sign_up_attachment_url = models.CharField(max_length=256)
    status = models.IntegerField()

    VERIFYING = 0
    VERIFIED = 1
    DISMISSED = 2


class PeriodScore(models.Model):
    period = models.ForeignKey(Period)
    team = models.ForeignKey(Team)
    score = models.IntegerField()


class Work(models.Model):
    question = models.ForeignKey(ExamQuestion)
    team = models.ForeignKey(Team)
    content_url = models.CharField(max_length=256)
    score = models.IntegerField(default=0)
