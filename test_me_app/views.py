from django.contrib import auth
from codex.baseview import APIView
from codex.baseerror import *
from codex.basedecorator import login_required
import time

from test_me import settings


# Create your views here.


class Login(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise ValidateError("Not login");

    def post(self):
        self.check_input('username', 'password');
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

    @login_required
    def post(self):
        self.check_input('file', 'destination')
        file = self.input['file'][0]
        new_name = self.input['destination'] + '/' + time.strftime('%Y%m%d%H%M%S') + '.' + file['name'].split('.')[-1]
        save_path = settings.MEDIA_ROOT + '/' + new_name
        save_file = open(save_path, 'w+b')
        if file.multiple_chunks():
            for chunk in file.chunks():
                save_file.write(chunk)
        else:
            save_file.write(file.read())
        save_file.close()
        return settings.get_url(settings.MEDIA_URL + new_name)


class UserType(APIView):

    @login_required
    def get(self):
        return self.request.user.user_type
