header_c.showheader = true;
header_c.shownav = false;
header_c.showpersonal = true;
header_c.showsearchbox = true;
header_c.link_list.push({
    alias : '登出',
    link : '#',
    action : function() {
        window.logout();
    }
})

var myaccount_c = new Vue({
    el : '#myaccount',
    data : {
        modifyinfo : false,
        avatar_filename : '',
        //api part, query userinfo from server
        //suggested that it should be processed outside this model and simply assign it in the next line
        //for every field, there should be a list for it :
        //{ type : '', name : '', content : ''}
        user : null,
        //api part
        //it is different for students and organizers
        contestlist : [],
        usertype : -1,
        username : 'unknown user',
        status_dic : ['审核失败', '审核中', '审核通过'],
        dic : {
            'description' : '简介',
            'nickname' : '昵称',
            'contactPhone' : '电话',
            'email' : '邮箱',
            'verifyStatus' : '认证状态',
            'group' : '组织',
            'gender' : '性别',
            'birthday' : '生日',
            'playerType' : '在读类型'
        },
        index : {
            '昵称' : 0,
            '邮箱' : 1,
            '电话' : 2,
            '性别' : 2.1,
            '生日' : 2.4,
            '在读类型' : 2.7,
            '组织' : 3,
            '简介' : 4,
            '认证状态' : 5
        },
        player_type_dic : ['本科生', '研究生', '专科生', '高中生', '校外人员'],
        gender_type_dic : {
            'male' : '男',
            'female' : '女'
        }        
    },
    methods : {
        activate_modify : function() {
            this.modifyinfo = true;
        },
        avatar_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.avatar_filename = files[0].name;
        },
        modify_confirm : function() {
            if (myaccount_c.usertype == 1) {
                type_sign = 'o';
            }
            else if (myaccount_c.usertype == 0) {
                type_sign = 'p';
            }
            else {
                alert("Wrong user type!");
                return;
            }
            var url = '/api/'+ type_sign + '/personal_info';
            var m = 'POST';
            var data = {};
            for (i in myaccount_c.user) {
                if (myaccount_c.user[i].name == '认证状态') {
                    continue;
                }
                if (myaccount_c.user[i].name == '性别') {
                    data['gender'] = 'futa';
                    for (attr in myaccount_c.gender_type_dic) {
                        if (myaccount_c.gender_type_dic[attr] == myaccount_c.user[i].content) {
                            data['gender'] = attr;
                        }
                    }
                    continue;
                }
                if (myaccount_c.user[i].name == '在读类型') {
                    data['playerType'] = myaccount_c.player_type_dic.indexOf(myaccount_c.user[i].content);
                    continue;
                }
                for (name in myaccount_c.dic) {
                    if (myaccount_c.user[i].name == myaccount_c.dic[name]) {
                        data[name] = myaccount_c.user[i].content;
                    }
                }
            }
            data['avatarUrl'] = myaccount_c.avatar_filename;
            $t(url, m, data, this.modify_succ, this.modify_fail);
        },
        modify_succ : function(response) {
            alert('信息修改成功！');
            window.location.assign('index.html');
        },

        modify_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        },
        deletecontest : function(id) {
            //api
        },
        deletecontest_succ : function(response) {
            //api
        },
        deletecontest_fail : function(response) {
            //apdi
        },
        appeal : function(c_id) {
            //api
        },
        giveup : function(c_id) {
            //api
        },
        giveup_succ : function(response) {
            //api
        },
        giveup_fail : function(response) {
            //api
        },
        create_contest : function() {
            window.location.assign("../create-contest/index.html");
        }
    },
    computed : {
        avatar_url : function() {
            if (this.user != null) {
                for (attr in this.user)
                    if (attr.name == 'avatar_url')
                        return attr.content;
                return '../img/user.png';
            }
            return '../img/user.png';
        },
        user_name : function() {
            return this.username;
        },
        isorganizer : function() {
            return this.usertype == 1;
        }
    }
});

//$t(url, method, data, succ, fail)

function bigger(a, b) {
    return myaccount_c.index[a.name] > myaccount_c.index[b.name];
}

function get_personal_info() {
    if (myaccount_c.usertype == 1) {
        type_sign = 'o';
    }
    else if (myaccount_c.usertype == 0) {
        type_sign = 'p';
    }
    else {
        alert("Wrong user type!");
        return;
    }
    var url = '/api/'+ type_sign + '/personal_info';
    $t(url, 'GET', {}, 
        function (response) {
            myaccount_c.user = [];
            for (attr in response.data) {
                if (attr == 'avatarUrl') {
                    myaccount_c.avatar_filename = response.data[attr];
                }
                else if (attr == 'username') {
                    myaccount_c.username = response.data[attr];
                }
                else {
                    content = response.data[attr];
                    if (attr == 'verifyStatus') {
                        content = myaccount_c.status_dic[content + 1];
                    }
                    if (attr == 'gender') {
                        content = myaccount_c.gender_type_dic[content];
                    }
                    if (attr == 'playerType') {
                        content = myaccount_c.player_type_dic[content];
                    }
                    //{ type : '', name : '', content : ''}
                    myaccount_c.user.push({
                        type : 'text',
                        name : myaccount_c.dic[attr],
                        content : content
                    });
                }
            }
            myaccount_c.user.sort(bigger);
        },
        function (response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    );
}

function get_contest_info() {
    var url = '';
    if (myaccount_c.usertype == 1) {
        url = '/api/o/contest/organizing_contests';
        $t(url, 'GET', {}, 
            function (response) {
                for (i in response.data) {
                    myaccount_c.contestlist.push({
                        'name' : response.data[i].name,
                        'period' : response.data[i].creatorName,
                        'detail' : '#',
                        'id' : response.data[i].id,
                    });
                }
            },
            function (response) {
                alert('[' + response.code.toString() + ']' + response.msg);
            }
        );
    }
    else if (myaccount_c.usertype == 0) {
        url = '/api/p/participating_contests';
    }
    else {
        alert("Wrong user type!");
        return;
    }
}


(function () {
    //PLAYER = 0, ORGANIZER = 1
    myaccount_c.usertype = -1;
    $t('/api/c/user_type', 'GET', {},
        function (response) {
            myaccount_c.usertype = response['data'];
            get_personal_info();
            get_contest_info();
        },
        function (response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    );
})();
