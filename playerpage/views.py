from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User
from test_me_app.models import *
from test_me import settings
import time

# Create your views here.


class PlayerRegister(APIView):

    def post(self):
        self.check_input('username', 'password', 'email', 'gender', 'playerType', 'birthday')
        try:
            user = User.objects.create_user(username=self.input['username'],
                                            password=self.input['password'],
                                            email=self.input['email'])
            # avatar_url = settings.get_url(settings.STATIC_URL + 'img/default_avatar.jpg')
            gender = (self.input['gender'] == 'male')
            for v, k in Players.TYPE_CHOICE:
                if self.input['playerType'] == k:
                    player_type = v
                    break

            player = Players.objects.create(user=user,
                                            nickname=self.input['username'],
                                            gender=gender,
                                            player_type=player_type,
                                            birthday=self.input['birthday'])
        except:
            raise LogicError("Signup fail")