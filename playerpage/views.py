from codex.baseerror import *
from codex.baseview import APIView
from codex.basedecorator import *
from test_me_app.models import *
from test_me import settings

# Create your views here.


class PlayerRegister(APIView):

    def post(self):
        # check
        self.check_input('username', 'password', 'email', 'group', 'gender', 'playerType', 'birthday')
        if self.input['playerType'] < 0 or self.input['playerType'] > 4:
            raise InputError('Wrong player type')
        if self.input['gender'] not in ['male', 'female']:
            raise InputError('Wrong gender')
        # create
        try:
            user = User.objects.create_user(username=self.input['username'],
                                            password=self.input['password'],
                                            email=self.input['email'])
            user.user_type = User_profile.PLAYER
            user.save()
            # default columns
            avatar_url = settings.get_url(settings.STATIC_URL + 'img/default_avatar.jpg')
            description = '这个人很懒，什么都没有留下'
            # create player
            player = Player.objects.create(user=user,
                                           nickname=self.input['username'],
                                           group=self.input['group'],
                                           avatar_url=avatar_url,
                                           description=description,
                                           gender=(self.input['gender'] == 'male'),
                                           player_type=self.input['playerType'],
                                           birthday=self.input['birthday'])
            player.save()
        except:
            raise LogicError('Signup fail')
