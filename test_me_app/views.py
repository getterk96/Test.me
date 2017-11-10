from django.contrib import auth
from codex.baseview import APIView
from codex.baseerror import *
from datetime import datetime
import time

from test_me import settings
from test_me_app.models import *

# Create your views here.


class Index(APIView):

    def get(self):
        user = self.request.user
        try:
            avatar_url = user.player.avatar_url
        except:
            avatar_url = user.organizer.avatar_url
        return {'is_authenticated': bool(user.is_authenticated),
                'username': user.username,
                'id': user.id,
                'avatar_url': avatar_url}


class UserLogin(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise ValidateError("Not login");

    def post(self):
        self.check_input('username', 'password');
        user = auth.authenticate(username=self.input['username'], password=self.input['password'])
        if not user:
            raise ValidateError("Wrong username or password")
        auth.login(self.request, user)


class UserLogout(APIView):

    def post(self):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
        else:
            raise LogicError("Not login")


class PlayerSignup(APIView):

    def post(self):
        self.check_input('avatar-url', 'birthday-day', 'birthday-month', 'birthday-year',
                         'description', 'gender', 'group', 'nickname', 'password', 'phone',
                         'player-type', 'username');
        user = User.objects.create_user(username=self.input['username'],
                                        password=self.input['password'])
        type = 0
        for key, value in Players.TYPE_CHOICE:
            if value == self.input['player-type']:
                type = key
        player = Players.objects.create(user=user,
                                        group=self.input['group'],
                                        nickname=self.input['nickname'],
                                        avatar_url=self.input['avatar-url'],
                                        contact_phone=self.input['phone'],
                                        description=self.input['description'],
                                        gender=self.input['gender'],
                                        birthday=datetime(int(self.input['birthday-year']),
                                                             int(self.input['birthday-month']),
                                                             int(self.input['birthday-day'])),
                                        player_type=type)
        player.save()


class OrganizerSignup(APIView):

    def post(self):
        self.check_input('avatar-url', 'description', 'group', 'nickname', 'password', 'phone',
                         'verify-file-url', 'username')
        user = User.objects.create_user(username=self.input['username'],
                                        password=self.input['password'])
        organizer = Organizers.objects.create(user=user,
                                        group=self.input['group'],
                                        nickname=self.input['nickname'],
                                        avatar_url=self.input['avatar-url'],
                                        contact_phone=self.input['phone'],
                                        description=self.input['description'],
                                        verify_file_url=self.input['verify-file-url'],
                                        verify_status=Organizers.VERIFYING)
        organizer.save()


class UploadFile(APIView):

    def post(self):
        self.check_input('file_type', 'file')
        file = self.input['file'][0]
        new_name = self.input['file_type'] + '/' + time.strftime('%Y%m%d%H%M%S') + '.' + file.name.split('.')[-1]
        save_path = settings.MEDIA_ROOT + '/' + new_name
        save_file = open(save_path, 'w+b')
        if file.multiple_chunks():
            for chunk in file.chunks():
                save_file.write(chunk)
        else:
            save_file.write(file.read())
        save_file.close()
        return settings.get_url(settings.MEDIA_URL + new_name)


class UserCenter(APIView):

    def get(self):
        self.check_input('id')
        user = User.objects.get(id=self.input['id'])
        return {
            'username': user.username,
            'nickname': user.player.nickname
        }