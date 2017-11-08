from django.contrib import auth
from codex.baseview import APIView
from codex.baseerror import *

# Create your views here.


class Index(APIView):

    def get(self):
        user = self.request.user
        return {'is_authenticated': bool(user.is_authenticated),
                'username': user.username}


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
