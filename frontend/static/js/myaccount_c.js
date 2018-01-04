const type_p = 0;
const type_o = 1;
var player_type_dic = ['本科生', '研究生', '专科生', '高中生', '校外人员'];
var gender_type_dic = {'male' : '男', 'female' : '女'};
var gender_dic_rev = {'男' : 'male', '女' : 'female'};
var status_dic = ['未通过', '审核中', '已审核'];
var tmp = {};
var controller = {};

var nav = new Vue({
    el : '#side-nav',
    data : {
        list : [],
        choice : ''
    },
    methods : {
        select : function(target) {
            for (i of this.list)
                if (i == target) {
                    this.choice = target;
                    return;
                }
            console.log('[err] No such item');
        }
    }
})

var type_get_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var player_get_succ = function(response) {
    window.user = {
        avatar : {
            editable : true,
            link : response.data['avatarUrl']
        },
        nickname : {
            editable :true,
            content : response.data['nickname']
        },
        username : {
            editable : false,
            content : response.data['username']
        },
        org : {
            editable : false,
            content : response.data['group']
        },
        email : {
            editable : true,
            content : response.data['email']
        },
        type : {
            editable : false,
            content : player_type_dic[response.data['playerType']]
        },
        gender : {
            editable : false,
            content : gender_type_dic[response.data['gender']]
        },
        birthday : {
            editable : true,
            content : response.data['birthday']
        },
        description : {
            editable : true,
            content : response.data['description']
        }
    }
    init_header();
    init_controller();
}

var organizer_get_succ = function(response) {
    window.user = {
        avatar : {
            editable : true,
            link : response.data['avatarUrl']
        },
        nickname : {
            editable :true,
            content : response.data['nickname']
        },
        username : {
            editable : false,
            content : response.data['username']
        },
        org : {
            editable : false,
            content : response.data['group']
        },
        email : {
            editable : true,
            content : response.data['email']
        },
        description : {
            editable : true,
            content : response.data['description']
        },
        status : {
            editable : false,
            content : status_dic[response.data['verifyStatus'] + 1]
        }
    }
    init_header();
    init_controller();
}

var player_get_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var organizer_get_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var type_get_succ = function(response) {
    window.usertype = response.data;
    if (window.usertype == type_p) {
        var url = '/api/p/personal_info';
        var m = 'GET';
        var data = {};
        $t(url, m, data, player_get_succ, player_get_fail);
    }
    if (window.usertype == type_o) {
        var url = '/api/o/personal_info';
        var m = 'GET';
        var data = {};
        $t(url, m, data, organizer_get_succ, organizer_get_fail);
    }
}

var init = function () {
    var url = '/api/c/user_type';
    var m = 'GET';
    var data = {};
    $t(url, m, data, type_get_succ, type_get_fail);
};

init();

var init_header = function() {
    header.greeting = 'Test.Me';
    header.title = '个人中心';

    if (usertype in [0, 1]) {
        header.link_list.push({
            alias : '登出',
            link : '#',
            action : function() {
                logout();
            }
        });
    } else
        header.link_list.push({
            alias : '登录',
            link : '../index.html',
            action : empty_f
        })
    if (usertype == type_p) {
        nav.list = ['个人信息', '我的比赛', '我收到的组队邀请'];
        nav.choice = '个人信息';
    } else {
        nav.list = ['个人信息', '我的比赛'];
        nav.choice = '个人信息';
    }
};

var avatar_upload_pass = function(response) {
    controller.user.avatar.link = response.data;
    controller.save_modify_basic_info();
}

var avatar_upload_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var save_succ = function(response) {
    alert('信息修改成功！');
    controller.modify_basic_info = false;
}

var save_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var get_contest_succ = function(response) {
    var data = response.data;
    for (i in data) {
        var contest = {
            logo : data[i]['logoUrl'],
            id : data[i]['id'],
            name : data[i]['name']
        }
        controller.mycontest.push(contest);
    }
}

var get_contest_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var get_invi_succ = function(response) {
    var data = response.data;
    for (i in data) {
        var team = {
            name : data[i]['teamName'],
            id : data[i]['id'],
            cid : data[i]['contestId'],
            type : 'invite'
        }
        controller.myteam.push(team);
    }
}

var get_invi_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var get_contest = function() {
    var url = '';
    var m = 'GET';
    var data = {};
    if (window.usertype == type_o) {
        url = '/api/o/contest/organizing_contests';
    }
    if (window.usertype == type_p) {
        url = '/api/p/participating_contests';
    }
    $t(url, m, data, get_contest_succ, get_contest_fail);
}

var get_teams = function() {
    var url = '/api/p/team/invitation';
    var m = 'GET';
    var data = {};
    $t(url, m, data, get_invi_succ, get_invi_fail);
}

var init_controller = function() {
controller = new Vue({
    el : '#body',
    data : {
        user : window.user,
        modify_basic_info : false,
        modify_password : false,
        reupload_doc :false,
        password : '',
        cpassword : '',
        doc_name : '',
        mycontest : [],
        myteam : [],
        modify_description : false,
    },
    computed : {
        page : function() {
            return nav.choice;
        },
        user_type : function() {
            return window.usertype;
        }
    },
    methods : {
        uploadavatar : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'avatar');
            $t(url, m, data, avatar_upload_pass, avatar_upload_fail);
        },
        start_modify_basic_info : function() {
            this.modify_basic_info = true;
            tmp = {};
            tmp['nickname'] = this.user.nickname.content;
            tmp['email'] = this.user.email.content;
            if (window.usertype == type_p) {
                tmp['birthday'] = this.user.birthday.content;
            }
        },
        cancel_modify_basic_info : function() {
            this.modify_basic_info = false;
            this.user.nickname.content = tmp['nickname'];
            this.user.email.content = tmp['email'];
            this.user.birthday.content  = tmp['birthday'];
        },
        save_modify_basic_info : function() {
            var url = '';
            var m = 'POST';
            var data = {};
            if (window.usertype == type_o) {
                url = '/api/o/personal_info';
                data = {
                    'nickname' : this.user.nickname.content,
                    'avatarUrl' : this.user.avatar.link,
                    'description' : this.user.description.content,
                    'contactPhone' : '13000000000',
                    'email' : this.user.email.content,
                    'group' : this.user.org.content,
                };
            }
            if (window.usertype == type_p) {
                url = '/api/p/personal_info';
                data = {
                    'email' : this.user.email.content,
                    'group' : this.user.org.content,
                    'nickname' : this.user.nickname.content,
                    'avatarUrl' : this.user.avatar.link,
                    'contactPhone' : '13000000000',
                    'description' : this.user.description.content,
                    'gender' : gender_dic_rev[this.user.gender.content],
                    'birthday' : this.user.birthday.content,
                    'playerType' : player_type_dic.indexOf(this.user.type.content)
                };
            }
            $t(url, m, data, save_succ, save_fail);
        },
        switch_modify_password : function() {
            this.modify_password = !this.modify_password;
            this.password = '';
            this.cpassword = '';
        },
        switch_reupload_doc : function() {
            this.reupload_doc = !this.reupload_doc;
            this.doc_name = '';
        },
        save_password : function() {
            if (this.password != this.cpassword) {
                alert("两次输入密码不一致。");
                return;
            }
            var url = '/api/c/change_password';
            var m = 'POST';
            var data = {'password' : this.password};
            $t(url, m, data, this.save_password_succ, this.save_password_fail);
            this.switch_modify_password();
        },
        save_password_succ : function(response) {
            alert("密码修改成功。请重新登录。");
            window.location.assign('../index.html');
        },
        save_password_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        },
        reupload_val_doc : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.doc_name = files[0].name;
        },
        view_contest : function(cid) {
            var url = '';
            if (window.usertype == type_o) {
                url = '../cdetail/o/index.html?cid=' + cid.toString();
            }
            if (window.usertype == type_p) {
                url = '../cdetail/g/index.html?cid=' + cid.toString();
            }
            window.location.assign(url);
        },
        accept_invite : function(tid) {},
        deny_invite : function(tid) {},
        create_contest : function() {
            //check whether this user has the authentication to create a contest
            window.location.assign('../create-contest/index.html');
        },
        start_modify_description : function() {
            this.modify_description  = true;
            tmp['description'] = this.user.description.content;
        },
        cancel_modify_description : function() {
            this.modify_description = false;
            this.user.description.content = tmp['description'];
        },
        save_description : function() {
            //todo
        }
    }
})
    get_contest();
    if (window.usertype == type_p){
        get_teams();
    }
}
