from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, UserManager


# Create your models here.

class User_common(models.Model):
    #objects = UserManager()
    group = models.CharField(max_length = 128)
    # for players, group may mean their university or so
    # for organizers, group may mean their coporation or university or so
    nickname = models.CharField(max_length = 20)
    avatar_url = models.CharField(max_length=256)
    contact_phone = models.CharField(max_length = 20)
    description = models.TextField()

    class Meta:
        abstract = True


class Players(User_common):
    user = models.OneToOneField('auth.User', related_name='player')
    gender = models.BooleanField()
    birthday = models.DateField()
    TYPE_CHOICE = (
        (0, '本科生'),
        (1, '研究生'),
        (2, '专科生'),
        (3, '高中生'),
        (4, '校外人员'),
    )
    player_type = models.IntegerField(choices = TYPE_CHOICE)


class Organizers(User_common):
    user = models.OneToOneField('auth.User', related_name='organizer')
    verify_status = models.IntegerField()
    verify_file_url = models.CharField(max_length=256)
    
    VERIFYING = 0
    VERIFIED = 1
    REJECTED = 2


class Exam_questions(models.Model):
    description = models.TextField()
    attachment_url = models.CharField(max_length=256)
    submission_limit = models.IntegerField()


class Periods(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length = 20)
    available_slots = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()
    attachment_url = models.CharField(max_length=256)
    questions = models.ForeignKey(Exam_questions, null = True)


class Contests(models.Model):
    name = models.CharField(max_length = 64)
    description = models.TextField()
    logo_url = models.CharField(max_length=256)
    banner_url = models.CharField(max_length=256)
    sign_up_start_time = models.DateTimeField()
    sign_up_end_time = models.DateTimeField()
    available_slots = models.IntegerField()
    max_team_members = models.IntegerField()
    sign_up_attachment_url = models.CharField(max_length=256)
    level = models.CharField(max_length = 20)
    tags = models.ManyToManyField('Tags',
        related_name = 'contest_with_tag',
        related_query_name = 'contest_with_tag')
    periods = models.ForeignKey(Periods, related_name = 'contest', null = True)
    status = models.IntegerField()

    STATUS_DELETED = -1
    STATUS_SAVED = 0
    STATUS_PUBLISHED = 1

class Tags(models.Model):
    content = models.CharField(max_length = 20)


class Period_score(models.Model):
    period_id = models.IntegerField()
    team_id = models.IntegerField()
    score = models.IntegerField()
    rank = models.IntegerField()


class Works(models.Model):
    question_id = models.IntegerField()
    team_id = models.IntegerField()
    content_url = models.CharField(max_length=256)
    index = models.IntegerField()


class Teams(models.Model):
    players = models.ForeignKey(Players, null = True)
    leader_id = models.IntegerField()
    contest_id = models.IntegerField()
    avatar_url = models.CharField(max_length=256)
    description = models.TextField()
    status = models.IntegerField()
    score_record = models.ForeignKey(Period_score, null = True)
    works = models.ForeignKey(Works, null = True)
    sign_up_attachment_url = models.CharField(max_length=256)
