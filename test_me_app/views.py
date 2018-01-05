import time
import datetime

from django.contrib import auth
from codex.baseview import APIView
from codex.baseerror import *
from codex.basedecorator import login_required
from django.contrib.auth.models import User
from test_me_app.models import Contest, ForumPost, ForumReply

from test_me import settings


# Create your views here.


class Login(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise ValidateError("Not login")

    def post(self):
        self.check_input('username', 'password')
        user = auth.authenticate(username=self.input['username'], password=self.input['password'])
        if not user:
            raise ValidateError("Wrong username or password")
        auth.login(self.request, user)


class Logout(APIView):

    def post(self):
        if self.request.user.is_authenticated:
            try:
                auth.logout(self.request)
            except:
                raise LogicError("Logout fail")


class Upload(APIView):

    def post(self):
        self.check_input('file', 'destination')
        try:
            file = self.input.get('file')[0]
            new_name = self.input.get('destination') + '\\' + time.strftime('%Y%m%d%H%M%S') + '.' + file.name.split('.')[-1]
            save_path = settings.MEDIA_ROOT + '\\' + new_name
            save_file = open(save_path, 'w+b')
            if file.multiple_chunks():
                for chunk in file.chunks():
                    save_file.write(chunk)
            else:
                save_file.write(file.read())
            save_file.close()
        except:
            raise LogicError('Upload failed')
        return 'http://' + settings.SITE_DOMAIN + '/media/' + new_name


class UserType(APIView):

    @login_required
    def get(self):
        return self.request.user.user_profile.user_type

        
class ChangePassword(APIView):

    @login_required
    def post(self):
        self.check_input('password')
        self.request.user.set_password(self.input['password'])
        self.request.user.save()

class UserId(APIView):

    @login_required
    def get(self):
        return self.request.user.id

class ForumList(APIView):

    #@login_required
    def get(self):
        default_page_posts = 5
        # check existence
        self.check_input('contest_id', 'page')
        page = int(self.input['page'])
        contest_id = int(self.input['contest_id'])
        contest = Contest.safe_get(id=contest_id)
        dbposts = contest.forumpost_set.all()
        count = dbposts.count()
        if count % default_page_posts == 0:
            max_len = count / default_page_posts
            if max_len == 0:
                max_len = 1
        else:
            max_len = count // default_page_posts + 1
        posts = []
        if (page - 1) * default_page_posts + 1 <= count:
            if page * default_page_posts > count:
                if (page - 1) * default_page_posts == count - 1 :
                    posts.append(dbposts[(page - 1) * default_page_posts])
                else:
                    posts = dbposts[(page - 1) * default_page_posts: count]
            else:
                posts = dbposts[(page - 1) * default_page_posts: page * default_page_posts]
        cur_page_posts = []

        for post in posts:
            #user = None
            #if post.user.user_profile.user_type == 0:
            #    user = post.user.player
            #elif user.user_profile.user_type == 1:
            #    user = post.user.organizer
            #else:
            #    raise LogicError('The system administrator shouldn\'t be allowed to post posts in the forum.')
            cur_page_posts.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'createTime': post.create.strftime("%Y-%m-%d %H:%M:%S"),
                'authorName': post.user.username
            })
        return {
            'contestName': contest.name,
            'maxLen': max_len,
            'posts': cur_page_posts
        }


class ForumPostCreate(APIView):

    #@login_required
    def post(self):
        # check existence
        self.check_input('title', 'content', 'user_id', 'contest_id')
        post = ForumPost()
        post.title = self.input['title']
        post.content = self.input['content']
        post.user = User.objects.get(id=self.input['user_id'])
        post.contest = Contest.objects.get(id=self.input['contest_id'])
        post.save()
        return post.id


class ForumDetail(APIView):

    #@login_required
    def get(self):
        default_page_replies = 5
        # check existence
        self.check_input('user_id', 'post_id', 'page')
        # check validation
        try:
            user = User.objects.get(id=self.input['user_id'])
        except:
            raise LogicError('No Such User')
        try:
            post = ForumPost.objects.get(id=self.input['post_id'])
        except:
            raise LogicError('No Such Post')
        page = int(self.input['page'])
        count = post.forumreply_set.all().count()
        if count % default_page_replies == 0:
            max_len = count / default_page_replies
            if max_len == 0:
                max_len = 1
        else:
            max_len = count // default_page_replies + 1
        replies = []
        if (page - 1) * default_page_replies + 1 <= count:
            if page * default_page_replies > count:
                if (page - 1) * default_page_replies == count - 1 :
                    replies.append(post.forumreply_set.all()[(page - 1) * default_page_replies])
                else:
                    replies = post.forumreply_set.all()[(page - 1) * default_page_replies: count]
            else:
                replies = post.forumreply_set.all()[(page - 1) * default_page_replies: page * default_page_replies]
        cur_page_replies = []
        #user = None
        #if user.user_profile.user_type == 0:
        #    user = user.player
        #elif user.user_profile.user_type == 1:
        #    user = user.organizer
        #else:
        #    raise LogicError('The system administrator is not allowed to open posts in the forum')

        for reply in replies:
            cur_page_replies.append({
                'id': reply.id,
                'title': reply.title,
                'content': reply.content,
                'createTime': reply.create.strftime("%Y-%m-%d %H:%M:%S"),
                'authorName': reply.user.username
            })
        return {
            'maxLen': max_len,
            'title': post.title,
            'content': post.content,
            'createTime': post.create.strftime("%Y-%m-%d %H:%M:%S"),
            'authorName': post.user.username,
            'replies': cur_page_replies
        }

class ForumReplyCreate(APIView):

    #@login_required
    def post(self):
        # check existence
        self.check_input('title', 'content', 'user_id', 'post_id')
        reply = ForumReply()
        reply.title = self.input['title']
        reply.content = self.input['content']
        reply.user = User.objects.get(id=self.input['user_id'])
        reply.post = ForumPost.objects.get(id=self.input['post_id'])
        reply.save()
        return reply.id
    
class ForumMessages(APIView):

    #@login_required
    def get(self):
        # check existence
        self.check_input('id', 'page')
        # check validation
        try:
            user = User.objects.get(id=self.input['id'])
        except:
            raise LogicError('No such user')
        max_len = user.forumpost_set.all().count()
        posts = []
        if (self.input['page'] - 1) * 5 + 1 <= max_len:
            if self.input['page'] * 5 > max_len:
                posts = user.forumpost_set.all()[(self.input['page'] - 1) * 5, max_len - 1]
            else:
                posts = user.forumpost_set.all()[(self.input['page'] - 1) * 5, self.input['page'] * 5 - 1]
        cur_page_posts = []
        user = None
        if user.user_profile.user_type == 0:
            user = user.player
        elif user.user_profile.user_type == 1:
            user = user.organizer
        else:
            raise LogicError('The system administrator is not allowed to open posts in the forum')

        for post in posts:
            cur_page_posts.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'createTime': post.create,
            })
        return {
            'maxLen': max_len,
            'posts': posts
        }
