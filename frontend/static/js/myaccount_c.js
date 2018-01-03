const type_p = 0;
const type_o = 1;

window.usertype = type_p;

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

var init_header = function() {
    header.greeting = 'Test.Me';
    header.title = '个人中心';

    if (usertype in [0, 1]) {
        header.link_list.push({
            alias : '比赛大厅',
            link : '../index/index.html',
            action : empty_f
        });
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
        nav.list = ['个人信息', '我的比赛', '我的队伍'];
        nav.choice = '个人信息';
    } else {
        nav.list = ['个人信息', '我的比赛'];
        nav.choice = '个人信息';
    }
};


init_header();

var tmp = {};

window.user = {
    avatar : {
        editable : true,
        link : "../img/default_avatar.jpg"
    },
    nickname : {
        editable :true,
        content : 'Ica Riluci'
    },
    username : {
        editable : false,
        content : 'ica_riluci'
    },
    org : {
        editable : false,
        content : 'thu'
    },
    email : {
        editable : true,
        content : 'ica.riluci@gmail.com'
    },
    type : {
        editable : false,
        content : '本科生'
    },
    gender : {
        editable : false,
        content : '男'
    },
    birthday : {
        editable : true,
        content : '1997-03-15'
    },
    status : {
        editable : false,
        content : '未通过'
    }
}

var controller = new Vue({
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
        myteam : []
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
        clearsearchbox : function() {
            this.querytext = '';
        },
        searchcontest : function() {
            console.log("you're querying contest " + this.querytext);
        },
        randomcontest : function() {
            console.log("return a random contest");
        },
        uploadavatar : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            alert('succeed!')
        },
        start_modify_basic_info : function() {
            this.modify_basic_info = true;
            tmp = {};
            tmp['nickname'] = this.user.nickname.content;
            tmp['email'] = this.user.email.content;
            tmp['birthday'] = this.user.birthday.content;
        },
        cancel_modify_basic_info : function() {
            this.modify_basic_info = false;
            this.user.nickname.content = tmp['nickname'];
            this.user.email.content = tmp['email'];
            this.user.birthday.content  = tmp['birthday'];
        },
        save_modify_basic_info : function() {},
        switch_modify_password : function() {
            this.modify_password = !this.modify_password;
            this.password = '';
            this.cpassword = '';
        },
        switch_reupload_doc : function() {
            this.reupload_doc = !this.reupload_doc;
            this.doc_name = '';
        },
        save_password : function() {},
        reupload_val_doc : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.doc_name = files[0].name;
        },
        view_contest : function(cid) {},
        accept_invite : function(tid) {},
        deny_invite : function(tid) {}
    }
})
