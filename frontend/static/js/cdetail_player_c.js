window.cid = window.get_args('cid');

window.usertype = 0;
window.problem_list_ready = false;

var level_dic = ["国际级", "国家级", "省级", "市级", "区级", "校级", "院系级"];
var status_dic = ["未报名", "审核中", "审核通过"];
var info = {};

const type_p = 0;
const type_o = 1;

function period_get_succ(response, param) {
    var start_time = new Date(response.data['startTime']*1000);
    var end_time = new Date(response.data['endTime']*1000);
    var period =   {
        show : true,
        attr : [
            {
                name : 'name',
                alias : '阶段名称',
                type : 'text',
                content : response.data['name'],
                editable : true
            },
            {
                name : 'description',
                alias : '阶段简介',
                type : 'ltext',
                content : response.data['description'],
                editable : true
            },
            {
                name : 'stime',
                alias : '开始时间',
                type : 'datetime',
                content : {
                    d : start_time.getFullYear() + '-' + (start_time.getMonth() < 9 ? '0' : '') + (start_time.getMonth() + 1) + '-' + (start_time.getDate() < 10 ? '0' : '') + start_time.getDate(),
                    h : start_time.getHours(),
                    m : start_time.getMinutes()
                },
                editable : true
            },
            {
                name : 'etime',
                alias : '结束时间',
                type : 'datetime',
                content : {
                    d : end_time.getFullYear() + '-' + (end_time.getMonth() < 9 ? '0' : '') + (end_time.getMonth() + 1) + '-' + (end_time.getDate() < 10 ? '0' : '') + end_time.getDate(),
                    h : end_time.getHours(),
                    m : end_time.getMinutes()
                },
                editable : true
            },
            {
                name : 'p_file',
                alias : '阶段附件',
                editable : true,
                type : 'file',
                content : {
                     url : response.data['attachmentUrl'],
                     filename : response.data['attachmentUrl']
                 }
            }
        ],
        start_time : response.data['startTime']*1000,
        end_time : response.data['endTime']*1000,
        id : param['id'],
        name : response.data['name']
    }
    window.contest.period.push(period);
}

function period_get_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function qlist_get_succ(response, param) {
    window.plist = {
        period : param['name'],
        problems : []
    };
    //submission_limit sub_mission_times
    for (i of response.data){
        question = {
            description: i['description'],
            show: true,
            attachment: {
                filename : i['attachmentUrl'],
                url : i['attachmentUrl']
            },
            answer : i['workUrl'],
            id : i['id']
        }
        window.plist.problems.push(question);
    }
    init_header();
}

function qlist_get_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function user_id_succ(response) {
    window.user_id = response.data;
    var now = (new Date()).valueOf();
    var flag = 0;
    for (i of window.contest.period) {
        if (i.start_time <= now && now <= i.end_time) {
            flag = 1;
            problem_list_ready = true;
            var url = '/api/p/question/detail';
            var m = 'GET';
            var data = {'pid' : i.id};
            $t(url, m, data, qlist_get_succ, qlist_get_fail, {'name': i.name});
        }
    }
    if (flag == 0) {
        problem_list_ready = false;
    }
}

function user_id_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function team_get_succ(response) {
    window.team = {
        name : response.data['name'],
        status : status_dic[response.data['status']],
        member : [{
            nickname : response.data['leader']['nickname'],
            avatar_url : response.data['leader']['avatarUrl'],
            school : response.data['leader']['group'],
            id : response.data['leader']['id'],
            accept : true,
        }],
        leader_id : response.data['leader']['id'],
        new_leader : '',
        attachment_url : response.data['signUpAttachmentUrl']
    }
    for (i of response.data['members']){
        var member = {
            nickname : i['nickname'],
            avatar_url : i['avatarUrl'],
            school : i['group'],
            id : i['id'],
            accept : (i['invitationStatus'] == 1),
        }
        window.team.member.push(member);
    }
    var url = '/api/c/user_id';
    var m = 'GET';
    var data = {};
    $t(url, m, data, user_id_succ, user_id_fail);
}

function team_get_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function team_list_succ(response) {
    for (i of response.data) {
        if (i['cid'] == window.cid) {
            window.team_id = i['id'];
            break;
        }
    }
    var url = '/api/p/team/detail';
    var m = 'GET';
    var data = {'tid' : window.team_id};
    $t(url, m, data, team_get_succ, team_get_fail);
}

function team_list_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function contest_get_succ(response) {
    var start_time = new Date(response.data['signUpStartTime']*1000);
    var end_time = new Date(response.data['signUpEndTime']*1000);
    window.contest = {
        getAttr : function(qname) {
            for (i of this.attr)
                if (i.name == qname)
                    return i.content;
            console.log('[err] No such attr');
            return null;
        },
        period : [],
        attr : [
            {
                name : 'name',
                alias : '比赛名称',
                type : 'text',
                content : response.data['name'],
                editable : true
            },
            {
                name : 'level',
                alias : 'level',
                type : 'text',
                content : level_dic[response.data['level']],
                editable : true
            },
            {
                name : 'description',
                alias : '比赛简介',
                type : 'ltext',
                content : response.data['description'],
                editable : true
            },
            {
                name : 'stime',
                alias : '报名开始时间',
                type : 'datetime',
                content : {
                    d : start_time.getFullYear() + '-' + (start_time.getMonth() < 9 ? '0' : '') + (start_time.getMonth() + 1) + '-' + (start_time.getDate() < 10 ? '0' : '') + start_time.getDate(),
                    h : start_time.getHours(),
                    m : start_time.getMinutes()
                },
                editable : true
            },
            {
                name : 'etime',
                alias : '报名结束时间',
                type : 'datetime',
                content : {
                    d : end_time.getFullYear() + '-' + (end_time.getMonth() < 9 ? '0' : '') + (end_time.getMonth() + 1) + '-' + (end_time.getDate() < 10 ? '0' : '') + end_time.getDate(),
                    h : end_time.getHours(),
                    m : end_time.getMinutes()
                },
                editable : true
            },
            {
                name : 'team_lim',
                alias : '团队人数上限',
                type : 'interval',
                content : {
                    min : '0',
                    max : response.data['maxTeamMembers']
                },
                editable : true
            },
            {
                name : 'slots',
                alias : '可报名团队数',
                type : 'number',
                content : response.data['availableSlots'],
                editable : true
            },
            {
                name : 'c_file',
                alias : '比赛附件',
                type : 'file',
                content : {
                    url : response.data['signUpAttachmentUrl'],
                    filename : response.data['signUpAttachmentUrl']
                }
            }
        ],
        period_modifier_available : true
    };
    window.periods = response.data['periods'];
    for (i in response.data['periods']) {
        var url = '/api/p/period/detail';
        var m = 'GET';
        var data = {'pid' : response.data['periods'][i]['periodId']};
        $t(url, m, data, period_get_succ, period_get_fail, {id : response.data['periods'][i]['periodId']});
    }
    var url = '/api/p/team/list';
    var m = 'GET';
    var data = {};
    $t(url, m, data, team_list_succ, team_list_fail);
}

function contest_get_fail(response) {
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
                var data = {'cid' : window.cid};
                $t(url, m, data, contest_get_succ, contest_get_fail);
            }
        },
        function (response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    );
})();

function switch_succ(response) {
    alert("移交队长成功！");
    location.reload();
}

function switch_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function save_succ(response) {
    alert("提交成功！");
}

function save_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function post_succ(response) {
    location.reload();
}

function post_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function upload_pass(response) {
    info.signup_material.attachment = response.data;
}

function upload_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function submit_succ(response) {
    alert('提交答案成功！');
}

function submit_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function answer_upload_pass(response, e) {
    for (item of info.problem_list.problems)
        if ('p-' + info.problem_list.problems.indexOf(item).toString() == e.target.id) {
            item.answer = response['data'];
            var url = '/api/p/question/submit';
            var m = 'POST';
            var data = {'workUrl':response['data'], 'qid': item.id};
            $t(url, m, data, submit_succ, submit_fail);
            break;
        }
}

function answer_upload_fail(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

/*
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
                    content : 'period 1',
                    editable : true
                },
                {
                    name : 'description',
                    alias : '阶段简介',
                    type : 'ltext',
                    content : 'description 1',
                    editable : true
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
                    editable : true
                },
                {
                    name : 'slots',
                    alias : '可参与团队数',
                    type : 'number',
                    content : '100',
                    editable : true
                },
                {
                    name : 'p_file',
                    alias : '阶段附件',
                    editable : true,
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
            content : 'contest 1',
            editable : true
        },
        {
            name : 'description',
            alias : '比赛简介',
            type : 'ltext',
            content : "The monks of Turstarkuri watched the rugged valleys below their mountain monastery as wave after wave of invaders swept through the lower kingdoms. Ascetic and pragmatic, in their remote monastic eyrie they remained aloof from mundane strife, wrapped in meditation that knew no gods or elements of magic. Then came the Legion of the Dead God, crusaders with a sinister mandate to replace all local worship with their Unliving Lord's poisonous nihilosophy. From a landscape that had known nothing but blood and battle for a thousand years, they tore the souls and bones of countless fallen legions and pitched them against Turstarkuri. The monastery stood scarcely a fortnight against the assault, and the few monks who bothered to surface from their meditations believed the invaders were but demonic visions sent to distract them from meditation. They died where they sat on their silken cushions. Only one youth survived--a pilgrim who had come as an acolyte, seeking wisdom, but had yet to be admitted to the monastery. He watched in horror as the monks to whom he had served tea and nettles were first slaughtered, then raised to join the ranks of the Dead God's priesthood. With nothing but a few of Turstarkuri's prized dogmatic scrolls, he crept away to the comparative safety of other lands, swearing to obliterate not only the Dead God's magic users--but to put an end to magic altogether.",
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
            alias : '团队人数limit',
            type : 'interval',
            content : {
                min : '5',
                max : '200'
            },
            editable : true
        },
        {
            name : 'slots',
            alias : '可报名团队数',
            type : 'number',
            content : '100',
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
    period_modifier_available : true
};*/

// window.user_id = 1;
/*
window.plist = {
    period : 'period1',
    problems : [
        {
            description : "The monks of Turstarkuri watched the rugged valleys below their mountain monastery as wave after wave of invaders swept through the lower kingdoms. Ascetic and pragmatic, in their remote monastic eyrie they remained aloof from mundane strife, wrapped in meditation that knew no gods or elements of magic. Then came the Legion of the Dead God, crusaders with a sinister mandate to replace all local worship with their Unliving Lord's poisonous nihilosophy. From a landscape that had known nothing but blood and battle for a thousand years, they tore the souls and bones of countless fallen legions and pitched them against Turstarkuri. The monastery stood scarcely a fortnight against the assault, and the few monks who bothered to surface from their meditations believed the invaders were but demonic visions sent to distract them from meditation. They died where they sat on their silken cushions. Only one youth survived--a pilgrim who had come as an acolyte, seeking wisdom, but had yet to be admitted to the monastery. He watched in horror as the monks to whom he had served tea and nettles were first slaughtered, then raised to join the ranks of the Dead God's priesthood. With nothing but a few of Turstarkuri's prized dogmatic scrolls, he crept away to the comparative safety of other lands, swearing to obliterate not only the Dead God's magic users--but to put an end to magic altogether.",
            show : true,
            attachment : {
                filename : 'fuck.pdf',
                url : '#'
            },
            answer : ''
        },
        {
            description : "The monks of Turstarkuri watched the rugged valleys below their mountain monastery as wave after wave of invaders swept through the lower kingdoms. Ascetic and pragmatic, in their remote monastic eyrie they remained aloof from mundane strife, wrapped in meditation that knew no gods or elements of magic. Then came the Legion of the Dead God, crusaders with a sinister mandate to replace all local worship with their Unliving Lord's poisonous nihilosophy. From a landscape that had known nothing but blood and battle for a thousand years, they tore the souls and bones of countless fallen legions and pitched them against Turstarkuri. The monastery stood scarcely a fortnight against the assault, and the few monks who bothered to surface from their meditations believed the invaders were but demonic visions sent to distract them from meditation. They died where they sat on their silken cushions. Only one youth survived--a pilgrim who had come as an acolyte, seeking wisdom, but had yet to be admitted to the monastery. He watched in horror as the monks to whom he had served tea and nettles were first slaughtered, then raised to join the ranks of the Dead God's priesthood. With nothing but a few of Turstarkuri's prized dogmatic scrolls, he crept away to the comparative safety of other lands, swearing to obliterate not only the Dead God's magic users--but to put an end to magic altogether.",
            show : true,
            attachment : {
                filename : 'fuck.pdf',
                url : '#'
            },
            answer : ''
        },
        {
            description : "The monks of Turstarkuri watched the rugged valleys below their mountain monastery as wave after wave of invaders swept through the lower kingdoms. Ascetic and pragmatic, in their remote monastic eyrie they remained aloof from mundane strife, wrapped in meditation that knew no gods or elements of magic. Then came the Legion of the Dead God, crusaders with a sinister mandate to replace all local worship with their Unliving Lord's poisonous nihilosophy. From a landscape that had known nothing but blood and battle for a thousand years, they tore the souls and bones of countless fallen legions and pitched them against Turstarkuri. The monastery stood scarcely a fortnight against the assault, and the few monks who bothered to surface from their meditations believed the invaders were but demonic visions sent to distract them from meditation. They died where they sat on their silken cushions. Only one youth survived--a pilgrim who had come as an acolyte, seeking wisdom, but had yet to be admitted to the monastery. He watched in horror as the monks to whom he had served tea and nettles were first slaughtered, then raised to join the ranks of the Dead God's priesthood. With nothing but a few of Turstarkuri's prized dogmatic scrolls, he crept away to the comparative safety of other lands, swearing to obliterate not only the Dead God's magic users--but to put an end to magic altogether.",
            show : true,
            attachment : {
                filename : 'fuck.pdf',
                url : '#'
            },
            answer : ''
        }
    ]
};

window.team = {
    name : '405',
    status : '未报名',
    member : [
        {
            nickname : 'hentaiZYN',
            avatar_url : '../../img/user.png',
            school : 'THU',
            id : '1',
            accept : true,
        },
        {
            nickname : 'o,manGJH',
            avatar_url : '../../img/user.png',
            school : 'THU',
            id : '2',
            accept : true
        }
    ],
    leader_id : '1',
    new_leader : ''
}*/


// window.usertype = 0;

var init_header = function(){

header.greeting = contest != null ? contest.getAttr('name') : 'Test.Me';
header.title = '比赛详情';

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

nav.list = ['比赛信息', '队伍信息', '我的申诉'];
nav.choice = '比赛信息';
if (problem_list_ready) { nav.list.push('比赛题目'); }

window.show_period = [true];

info = new Vue({
    el : '#body',
    data : {
        show_basic_info : true,
        show_member : true,
        team : window.team,
        contest : window.contest,
        signup_material : {
            attachment : window.team.attachment_url,
        },
        problem_list : window.plist,
        in_compose : false,
        in_check : false,
        appeal_title : '',
        appeal_type : 0,
        appeal_content : '',
        appeal_file : '',
        appeal_list : [
                {
                    reply : 'fuck gjh',
                    type : 1,
                    processed : 1,
                    title : 'fuck zyn',
                    content : 'fuckkkkkkkkkk zyn',
                    a_url : '#'
                },
                {
                    reply : '',
                    type : 0,
                    processed : 0,
                    title : 'fuck zyn',
                    content : 'fuckkkkkkkkkk zyn',
                    a_url : '#'
                }
        ],
        appeal_status_dict : ['未处理', '已处理'],
        appeal_type_dict : ['资格', '成绩'],
        appeal_oncheck : -1
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
        switch_member : function() {
            this.show_member = !this.show_member;
        },
        t_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.signup_material.attachment = files[0].name;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'team_sign_up_attachment');
            $t(url, m, data, upload_pass, upload_fail);
        },
        switch_period_info : function(idx) {
            this.contest.period[idx].show = !this.contest.period[idx].show;
        },
        get_p_name : function(idx) {
            for (i of this.contest.period[idx].attr)
                if (i.name == 'name')
                    return(i.content);
        },
        is_self : function(id) {
            return window.user_id == id;
        },
        visit_user : function(id) {
            if (this.is_self(id)) {
                //visit myaccount
            } else {
                //guest visit
            }
        },
        switch_team_ownership : function() {
            var lid = 0, tmp = 1;
            for(var i = this.team.new_leader.length - 2; this.team.new_leader[i] >= '0' && this.team.new_leader[i] <= '9'; i = i - 1) {
                lid = lid + (this.team.new_leader[i] - '0') * tmp;
                tmp = tmp * 10;
            }
            var member_ids = [];
            for (i of this.team.member)
                if (i.id != lid)
                    member_ids.push(i.id);
            var url = '/api/p/team/detail';
            var m = 'POST';
            var data = {
                'tid' : window.team_id,
                'leaderId' : lid,
                'memberIds' : member_ids,
                'avatarUrl' : '',
                'description' : '',
                'signUpAttachmentUrl' : this.signup_material.attachment
            };
            $t(url, m, data, switch_succ, switch_fail);
        },
        save : function() {
            var member_ids = [];
            for (i of this.team.member)
                if (i.id != this.team.leader_id)
                    member_ids.push(i.id);
            console.log(member_ids);
            var url = '/api/p/team/detail';
            var m = 'POST';
            var data = {
                'tid' : window.team_id,
                'leaderId' : window.team.leader_id,
                'memberIds' : member_ids,
                'avatarUrl' : '',
                'description' : '',
                'signUpAttachmentUrl' : this.signup_material.attachment
            };
            $t(url, m, data, save_succ, save_fail);
        },
        post : function() {
            this.save();
            var url = '/api/p/team/signup';
            var m = 'POST';
            var data = {'tid' : window.team_id};
            $t(url, m, data, post_succ, post_fail);
        },
        switch_problem_status : function(id) {
            this.problem_list.problems[id].show = !this.problem_list.problems[id].show;
        },
        upload_answer : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'team_sign_up_attachment');
            $t(url, m, data, answer_upload_pass, answer_upload_fail, e);
        },
        switch_compose : function() {
            this.in_compose = !this.in_compose;
        },
        select_appeal_type : function(t) {
            if (!t in [0, 1])
                return;
            this.appeal_type = t;
        },
        appeal_a_upload : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.appeal_file = files[0].name;
        },
        send_appeal : function() {},
        check_appeal : function(id) {
            this.appeal_oncheck = id;
            this.in_check = true;
        },
        close_a_check : function() {
            this.in_check = false;
        }
    }
});
}

// init_header();
