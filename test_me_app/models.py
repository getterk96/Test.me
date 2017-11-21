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


post_save.connect(create_user_profile, sender = User)


class User_common(models.Model):
    group = models.CharField(max_length=128)
    # for players, group may mean their university or so
    # for organizers, group may mean their coporation or university or so
    nickname = models.CharField(max_length=20)
    avatar_url = models.CharField(max_length=256)
    contact_phone = models.CharField(max_length=20, default="")
    description = models.TextField()
    
    class Meta:
        abstract = True


class Player(User_common):
    user = models.OneToOneField(User, related_name='player')
    gender = models.BooleanField()
    birthday = models.DateField()
    player_type = models.IntegerField()
    
    UNDERGRADUATE = 0
    POSTGRADUATE = 1
    JUNIOR_COLLEGE_STUDENT = 2
    HIGH_SCHOOL_STUDENT = 3
    OUTSIDER = 4


class Organizer(User_common):
    user = models.OneToOneField(User, related_name='organizer')
    verify_status = models.IntegerField()
    verify_file_url = models.CharField(max_length=256)
    
    VERIFYING = 0
    VERIFIED = 1
    REJECTED = -1


class Exam_question(models.Model):
    index = models.IntegerField()
    description = models.TextField()
    attachment_url = models.CharField(max_length=256)
    submission_limit = models.IntegerField()


class Period(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=20)
    available_slots = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()
    attachment_url = models.CharField(max_length=256)
    questions = models.ForeignKey(Exam_question, null = True)


class Contest(models.Model):
    name = models.CharField(max_length=64)
    creator_id = models.IntegerField()
    description = models.TextField()
    logo_url = models.CharField(max_length=256)
    banner_url = models.CharField(max_length=256)
    sign_up_start_time = models.DateTimeField()
    sign_up_end_time = models.DateTimeField()
    available_slots = models.IntegerField()
    max_team_members = models.IntegerField()
    sign_up_attachment_url = models.CharField(max_length=256)
    level = models.IntegerField()
    
    INTERNATIONAL = 0
    NATIONAL = 1
    PROVINCIAL = 2
    MUNICIPAL = 3
    DISTRICT = 4
    SCHOOL = 5
    DEPARTMENT = 6
    
    tags = models.ManyToManyField('Tag',
        related_name='contest_with_tag',
        related_query_name='contest_with_tag')
    periods = models.ForeignKey(Period, related_name='contest', null=True)
    status = models.IntegerField()
    
    CANCELLED = -1
    SAVED = 0
    PUBLISHED = 1


class Tag(models.Model):
    content = models.CharField(max_length=20)


class Period_score(models.Model):
    period_id = models.IntegerField()
    team_id = models.IntegerField()
    score = models.IntegerField()
    rank = models.IntegerField()


class Work(models.Model):
    question_id = models.IntegerField()
    team_id = models.IntegerField()
    content_url = models.CharField(max_length=256)
    index = models.IntegerField()
    score = models.IntegerField()


class Team(models.Model):
    players = models.ForeignKey(Player, null=True)
    leader_id = models.IntegerField()
    contest_id = models.IntegerField()
    avatar_url = models.CharField(max_length=256)
    description = models.TextField()
    status = models.IntegerField()
    score_record = models.ForeignKey(Period_score, null=True)
    works = models.ForeignKey(Work, null=True)
    sign_up_attachment_url = models.CharField(max_length=256)
