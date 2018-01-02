from django.contrib import auth
from codex.baseview import APIView
from codex.baseerror import *
from codex.basedecorator import login_required
import os
import time

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
        file = self.input['file'][0]
        new_name = time.strftime('%Y.%m.%d %H:%M:%S') + '.' + file.name.split('.')[-1]
        save_path = settings.MEDIA_ROOT + '/' + self.input['destination'] + '/'
        if not os.path.exists(settings.MEDIA_ROOT):
            os.mkdir(settings.MEDIA_ROOT)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        try:
            save_file = open(save_path + new_name, 'w+b')
        except:
            raise LogicError('Failed to save file' + file.name)
        if file.multiple_chunks():
            for chunk in file.chunks():
                save_file.write(chunk)
        else:
            save_file.write(file.read())
        save_file.close()
        return save_path + new_name


class UserType(APIView):

    @login_required
    def get(self):
        return self.request.user.user_profile.user_type
