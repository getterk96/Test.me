window.cid = window.get_args('cid');

window.usertype = -1;
window.invitation_counter = 0;

const type_p = 0;
const type_o = 1;
var info = {};

window.contest = {
    getAttr : function(qname) {
        for (i of this.attr)
            if (i.name == qname)
                return i.content;
        console.log('[err] No such attr');
        return null;
    },
    period : [
        {
            show : true,
            attr : [
                {
                    name : 'name',
                    alias : '阶段名称',
                    type : 'text',
                    content : '',
                    editable : false
                },
                {
                    name : 'description',
                    alias : '阶段简介',
                    type : 'ltext',
                    content : '',
                    editable : false
                },
                {
                    name : 'time',
                    alias : '阶段时间',
                    type : 'datetime',
                    content : {
                        sd : '1977-03-11',
                        ed : '1997-05-22',
                        sh : '19',
                        sm : '00',
                        eh : '19',
                        em : '00'
                    },
                    editable : false
                },
                {
                    name : 'slots',
                    alias : '可参与团队数',
                    type : 'number',
                    content : '',
                    editable : false
                },
                {
                    name : 'p_file',
                    alias : '阶段附件',
                    editable : false,
                    type : 'file',
                    content : {
                        url : '#',
                        filename : 'fuck-zyn.pdf'
                    }
                }
            ]
        }
    ],
    attr : [
        {
            name : 'name',
            alias : '比赛名称',
            type : 'text',
            content : '',
            editable : true
        },
        {
            name : 'description',
            alias : '比赛简介',
            type : 'ltext',
            content : "",
            editable : true
        },
        {
            name : 'time',
            alias : '报名时间',
            type : 'datetime',
            content : {
                sd : '1977-03-11',
                ed : '1997-05-22',
                sh : '19',
                sm : '00',
                eh : '19',
                em : '00'
            },
            editable : true
        },
        {
            name : 'team_lim',
            alias : '团队人数上限',
            type : 'number',
            content : '',
            editable : true
        },
        {
            name : 'slots',
            alias : '可报名团队数',
            type : 'number',
            content : '',
            editable : true
        },
        {
            name : 'c_file',
            alias : '比赛附件',
            type : 'file',
            content : {
                url : '#',
                filename : 'fuckzyn.pdf'
            }
        }
    ],
    period_modifier_available : false
};

window.invitation = [];

function ply_get_succ(response) {
    var data = response.data;
    if (data['alreadySignUp'] == 1) {
        window.location.assign('../p/index.html?cid=' + window.cid);
        return;
    }
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
            case 'time' :
                window.contest.attr[i].content['sd'] = start_time.getFullYear().toString() +
                    '-' + (start_time.getMonth() < 9 ? '0' : '') + (start_time.getMonth() + 1).toString() +
                    '-' + (start_time.getDate() < 10 ? '0' : '') + start_time.getDate().toString();
                window.contest.attr[i].content['sh'] = start_time.getHours().toString();
                window.contest.attr[i].content['sm'] = start_time.getMinutes().toString();
                window.contest.attr[i].content['ed'] = end_time.getFullYear().toString() +
                    '-' + (end_time.getMonth() < 9 ? '0' : '') + (end_time.getMonth() + 1).toString() +
                    '-' + (end_time.getDate() < 10 ? '0' : '') + end_time.getDate().toString();
                window.contest.attr[i].content['eh'] = end_time.getHours().toString();
                window.contest.attr[i].content['em'] = end_time.getMinutes().toString();
                break;
            case 'slots' :
                window.contest.attr[i].content = data['availableSlots'].toString();
                break;
            case 'team_lim' :
                window.contest.attr[i].content = data['maxTeamMembers'].toString();
                break;
            case 'c_file' :
                window.contest.attr[i].content.url = data['signUpAttachmentUrl'];
                window.contest.attr[i].content.file_name = data['signUpAttachmentUrl'];
                break;
        }
    }
    window.contest.period_counter = 0;
    window.contest.period_id = [];
    for(i in data['periods']) {
        window.contest.period_id.push(data['periods'][i].periodId);
    }
    window.contest.period = [];
    for (i in data['periods']) {
        var pdata = data['periods'][i];
        var start_time = new Date((pdata['periodStartTime'] - 8 * 3600) * 1000);
        var end_time = new Date((pdata['periodEndTime'] - 8 * 3600) * 1000);
        var period = {
            show : true,
            attr : [
                {
                    name : 'name',
                    alias : '阶段名称',
                    type : 'text',
                    content : pdata['periodName'],
                    editable : true,
                },
                {
                    name : 'time',
                    alias : '阶段时间',
                    type : 'datetime',
                    content : {
                        sd : start_time.getFullYear().toString() +
                            '-' + (start_time.getMonth() < 9 ? '0' : '') + (start_time.getMonth() + 1).toString() +
                            '-' + (start_time.getDate() < 10 ? '0' : '') + start_time.getDate().toString(),
                        ed : end_time.getFullYear().toString() +
                            '-' + (end_time.getMonth() < 9 ? '0' : '') + (end_time.getMonth() + 1).toString() +
                            '-' + (end_time.getDate() < 10 ? '0' : '') + end_time.getDate().toString(),
                        sh : start_time.getHours(),
                        sm : start_time.getMinutes(),
                        eh : end_time.getHours(),
                        em : end_time.getMinutes()
                    },
                    editable : true
                },
                {
                    name : 'slots',
                    alias : '可参与团队数',
                    type : 'number',
                    content : pdata['periodSlots'],
                    editable : true
                },
            ],
        }
        window.contest['period'].push(period)
    }
    //logoUrl bannerUrl level currentTime tags
    init_header();
    init_info();
}

function ply_get_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function inv_get_succ(response) {
    var invitations = response.data;
    for (i in invitations) {
        if (invitations[i].contestId == window.cid) {
            window.invitation_counter += 1;
            window.invitation.push({
                teamname : invitations[i].teamName,
                leadername : invitations[i].leaderName,
                leader_avatar_url : '../../img/user.png',
                tid : window.invitation_counter.toString(),
                id : invitations[i].id
            });
        }
    }
}

function inv_get_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

(function () {
    //PLAYER = 0, ORGANIZER = 1
    $t('/api/c/user_type', 'GET', {},
        function (response) {
            window.usertype = response['data'];
            if (window.usertype == type_p) {
                var url = '/api/p/contest/detail';
                var m = 'GET';
                var data = {cid : window.cid};
                $t(url, m, data, ply_get_succ, ply_get_fail);
                url = '/api/p/team/invitation';
                data = {};
                $t(url, m, data, inv_get_succ, inv_get_fail);
            }
        },
        function (response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    );
})();

//api
window.new_team = {
    name : '',
    member : []
}

var init_header = function() {
    if (usertype in [0, 1]) {
        header.link_list.push({
            alias : '比赛论坛',
            link : '../../forum/index.html?cid=' + window.cid,
            action : empty_f
        });
        header.link_list.push({
            alias : '个人中心',
            link : '../../myaccount/index.html',
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
        });
    if (usertype == type_p) {
        nav.list = ['比赛信息', '组队信息'];
        nav.choice = '比赛信息';
    }
    header.greeting = contest != null ? contest.getAttr('name') : 'Test.Me';
    header.title = '比赛详情';
}



var nav = new Vue({
    el : '#side-nav',
    data : {
        list : [],
        choice : '[null]'
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
});

window.show_period = [true];

var init_info = function() {
info = new Vue({
    el : '#body',
    data : {
        show_basic_info : true,
        show_invitations : true,
        invitation : window.invitation,
        new_team : window.new_team,
        accept_team : '',
        contest : window.contest
    },
    computed : {
        page : function() {
            return nav.choice;
        }
    },
    methods : {
        switch_basic_info : function() {
            this.show_basic_info = !this.show_basic_info;
        },
        switch_invitation : function() {
            this.show_invitations = !this.show_invitations;
        },
        switch_period_info : function(idx) {
            this.contest.period[idx].show = !this.contest.period[idx].show;
        },
        get_p_name : function(idx) {
            for (i of this.contest.period[idx].attr)
                if (i.name == 'name')
                    return(i.content);
        },
        remove_member : function(idx) {
            if ((idx >= this.new_team.length) || (idx < 0)) {
                console.log('[err] No such element');
                return;
            }
            this.new_team.member.splice(idx, 1);
        },
        insert_new_member : function() {
            if (this.new_team.member.length + 1 >= parseInt(this.contest.getAttr('team_lim'))) {
                return;
            }
            var new_member = { username : ''};
            this.new_team.member.push(new_member);
        },
        setpage : function(p) {
            for (np of nav.list)
                if (np == p) {
                    nav.choice = p;
                    return;
                }
            console.log('[err] No such page!');
        },
        create_team : function() {
            var url = '/api/p/team/create';
            var m = 'POST';
            var members = []
            for (i in this.new_team.member) {
                console.log(this.new_team.member[i].username);
                members.push(this.new_team.member[i].username);
            }
            var data = {
                'name' : this.new_team.name,
                'members' : members,
                'contestId' : window.cid,
                'avatarUrl' : '',
                'description' : '',
                'signUpAttachmentUrl' : ''
            };
            $t(url, m, data, this.create_team_succ, this.create_team_fail);
        },
        create_team_succ : function(response) {
            alert('已发送组队邀请！');
        },
        create_team_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        },
        confirm_join : function() {
            var str = info.accept_team;
            var unit = 1, now = 0, start = 0, end = 0;
            for (i = str.length - 1; i >= 0; i -= 1) {
                if (str[i] == ')' && start == 0) {
                    start = 1;
                }
                if (start == 1 && end == 0) {
                    if (str[i] < '0' || str[i] > '9') {
                        end = 1;
                    }
                    else {
                        now += unit * parseInt(str[i]);
                        unit *= 10;
                    }
                }
            }
            var url = '/api/p/team/invitation';
            var m = 'POST';
            var data = {'iid' : window.invitation[now].id, 'confirm' : 1};
            $t(url, m, data, this.confirm_succ, this.confirm_fail);
        },
        confirm_succ : function(response) {
            alert('加入成功！');
        },
        confirm_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    }
});
}
