window.users = [];
window.contests = [];

window.level_dic = ['国际级', '国家级', '省级', '市级', '区级', '校级', '院系级'];

window.contest = {
    status : 0,
    attr : [
        {
            name : 'name',
            alias : '比赛名称',
            type : 'text',
            content : 'niupi',
            editable : true
        },
        {
            name : 'level',
            alias : '比赛等级',
            type : 'text',
            content : 0,
            editable : true
        },
        {
            name : 'description',
            alias : '比赛简介',
            type : 'ltext',
            content : '111111111111111111111111111111111111',
            editable : true
        },
        {
            name : 'signupstime',
            alias : '报名开始时间',
            type : 'datetime',
            content : {
                d : '1999-01-01',
                h : '1',
                m : '1'
            }
        },
        {
            name : 'signupetime',
            alias : '报名结束时间',
            type : 'datetime',
            content : {
                d : '1999-01-01',
                h : '1',
                m : '1'
            }
        },
        {
            name : 'team_lim',
            alias : '团队人数上限',
            type : 'interval',
            content : {
                min : '0',
                max : '100'
            }
        },
        {
            name : 'slots',
            alias : '可报名团队数',
            type : 'number',
            content : '1'
        },
        {
            name : 'c_file',
            alias : '比赛附件',
            type : 'file',
            content : '#'
        },
        {
            name : 'c_logo',
            alias : '比赛logo',
            type : 'file',
            content : '#'
        },
        {
            name : 'c_banner',
            alias : '比赛横幅',
            type : 'file',
            content : '#'
        }
    ],
};

var org_get_fail = function(response) {
    alert('[' + response.code + ']' + response.msg);
}

var org_get_succ = function(response, id) {
    var user = {};
    user['id'] = id;
    user['status'] = response.data['verifyStatus'];
    user['attachment'] = response.data['verifyUrl'];
    user['description'] = response.data['description'];
    user['name'] = response.data['username'];
    users.push(user);
}

var user_get_succ = function(response) {
    var url = '/api/a/organzier/detail';
    var m = 'GET';
    for (i of response.data) {
        if (i['userType'] == 1) {
            var data = {id : i['id']};
            $t(url, m, data, org_get_succ, org_get_fail, i['id']);
        }
    }
}

var user_get_fail = function(response) {
    alert('[' + response.code + ']' + response.msg);
}

var con_get_succ = function(response, id) {
    var data = response.data;
    var start_time = new Date((data['signUpStartTime'] - 8 * 3600) * 1000);
    var end_time = new Date((data['signUpEndTime'] - 8 * 3600) * 1000);
    for (i in window.contest.attr) {
        switch (window.contest.attr[i].name) {
            case 'name' :
                window.contest.attr[i].content = data['name'];
                break;
            case 'description' :
                window.contest.attr[i].content = data['description'];
                break;
            case 'signupstime' :
                window.contest.attr[i].content['d'] = start_time.getFullYear().toString() +
                    '-' + (start_time.getMonth() < 9 ? '0' : '') + (start_time.getMonth() + 1).toString() +
                    '-' + (start_time.getDate() < 10 ? '0' : '') + start_time.getDate().toString();
                window.contest.attr[i].content['h'] = start_time.getHours().toString();
                window.contest.attr[i].content['m'] = start_time.getMinutes().toString();
                break;
            case 'signupetime' :
                window.contest.attr[i].content['d'] = end_time.getFullYear().toString() +
                    '-' + (end_time.getMonth() < 9 ? '0' : '') + (end_time.getMonth() + 1).toString() +
                    '-' + (end_time.getDate() < 10 ? '0' : '') + end_time.getDate().toString();
                window.contest.attr[i].content['h'] = end_time.getHours().toString();
                window.contest.attr[i].content['m'] = end_time.getMinutes().toString();
                break;
            case 'slots' :
                window.contest.attr[i].content = data['availableSlots'].toString();
                break;
            case 'team_lim' :
                window.contest.attr[i].content.max = data['maxTeamMembers'].toString();
                break;
            case 'c_file' :
                window.contest.attr[i].content.url = data['signUpAttachmentUrl'];
                window.contest.attr[i].content.file_name = data['signUpAttachmentUrl'];
                break;
            case 'level' :
                window.contest.attr[i].content = level_dic[data['level']];
                break;
            case 'c_logo' :
                window.contest.attr[i].content = data['logoUrl'];
                break;
            case 'c_banner' :
                window.contest.attr[i].content = data['bannerUrl'];
                break;
        }
    }
    window.contest.push(window.contest);
}

var con_get_fail = function(response) {
    alert('[' + response.code + ']' + response.msg);
}

var clist_get_succ = function(response) {
    var url = '/api/a/contest/detail';
    var m = 'GET';
    for (i of response.data) {
        data = {id : i['id']};
        $t(url, m, data, con_get_succ, con_get_fail, i['id']);
    }
};

var clist_get_fail = function(response) {
    alert('[' + response.code + ']' + response.msg);
};

(function() {
    var url = '/api/a/user/list';
    var m = 'GET';
    var data = {};
    $t(url, m, data, user_get_succ, user_get_fail);
    url = '/api/a/contest/list';
    $t(url, m, data, clist_get_succ, clist_get_fail);
})();

var empty_succ = function(response) {};

var empty_fail = function(response) {
    alert('[' + response.code + ']' + response.msg);
};

var logout_succ = function(response) {
    window.location.assign('index.html');
};

var ctrl = new Vue({
    el : '#backend',
    data : {
        user_process : true,
        user_list : window.users,
        contest_list : window.contests,
        selected_user : [],
        in_list : true,
        check_id : 0,
        ustatus_list : ['不通过', '通过'],
        cstatus_list : ['不通过', '通过']
    },
    methods : {
        check_contest : function(id) {
            this.check_id = id;
            this.in_list = false;
        },
        back_to_list : function() {
            this.in_list = true;
        },
        accept_user : function() {
            var url = '/api/a/organzier/verification';
            var m = 'POST';
            for (i of selected_user) {
                var data = {
                    id : i,
                    verify : 1
                }
                $t(url, m, data, empty_succ, empty_fail);
            }
            window.location.reload();
        },
        deny_user : function() {
            var url = '/api/a/organzier/verification';
            var m = 'POST';
            for (i of selected_user) {
                var data = {
                    id : i,
                    verify : 0
                }
                $t(url, m, data, empty_succ, empty_fail);
            }
            window.location.reload();
        },
        switch_plat : function () {
            this.user_process = !this.user_process;
        },
        accept_contest : function(cid) {
            var url = '/api/a/contest/verification';
            var m = 'POST';
            var data = {
                id : cid,
                verify : 1
            }
            $t(url, m, data, empty_succ, empty_fail);
            window.location.reload();
        },
        deny_contest : function(id) {
            var url = '/api/a/contest/verification';
            var m = 'POST';
            var data = {
                id : cid,
                verify : 0
            }
            $t(url, m, data, empty_succ, empty_fail);
            window.location.reload();
        },
        logout : function() {
            var url = '/api/c/logout'
            var m = "POST";
            var data = {};
            $t(url, m, data, logout_succ, empty_fail);
        }
    }
});

test_user = {
    name : 'wowo',
    description : 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    attachment : '#',
    status : 0,
    id : '1'
};
