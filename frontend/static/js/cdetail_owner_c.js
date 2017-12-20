window.cid = window.get_args('cid');

window.usertype = -1;

const type_p = 0;
const type_o = 1;

var info = {};

//api
/*
window.contest = {
    getAttr : function(qname) {
        for (i of this.attr)
            if (i.name == qname)
                return i.content;
        console.log('[err] No such attr');
        return null;
    },
    period_counter : 1,
    period_id : [],
    period : [],
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
            content : 'description 1',
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
            name : 'maxteam',
            alias : '团队人数上限',
            type : 'number',
            content : '100',
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
            name : 'processed',
            alias : '已审核',
            type : 'progress',
            content : {
                base : 'slots',
                value : '100'
            },
            editable : true
        },
        {
            name : 'c_file',
            alias : '比赛附件',
            type : 'file',
            content : ''
        }
    ],
    is_guest : false,
    period_modifier_available : true
};

var ques_get_succ = function(response, param) {
    var data = response.data;
    var n = param['which'];
    var question = {
        lid : (window.contest.period[n].question_counter + 1).toString(),
        attr : [
            {
                name : 'description',
                alias : '题目描述',
                type : 'ltext',
                editable : true,
                content : data['description']
            },
            {
                name : 'slots',
                alias : '提交次数上限',
                type : 'number',
                editable : true,
                content : data['submissionLimit'].toString()
             },
             {
                 name : 'q_file',
                 alias : '题目附件',
                 type : 'file',
                 editable : true,
                 content : data['attachmentUrl']
             }
        ]
    };
    window.contest.period[n].question.push(question);
    window.contest.period[n].question_counter += 1;
}

var ques_get_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var per_get_succ = function (response) {
    var data = response.data;
    var start_time = new Date(data['startTime'] * 1000);
    var end_time = new Date(data['endTime'] * 1000);
    var period = {
        lid : data['index'],
        attr : [
            {
                name : 'name',
                alias : '阶段名称',
                type : 'text',
                content : data['name'],
                editable : true,
            },
            {
                name : 'description',
                alias : '阶段简介',
                type : 'ltext',
                content : data['description'],
                editable : true
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
                content : data['availableSlots'],
                editable : true
            },
            {
                name : 'p_file',
                alias : '阶段附件',
                editable : true,
                type : 'file',
                content : data['attachmentUrl']
            }
        ],
        question_modifier_available : true,
        question_counter : 0,
        question : [],
        question_id : data['questionId'],
    }
    window.contest.period.push(period);
    window.contest.period_counter += 1;
    for (i in data['questionId']) {
        var url = '/api/o/question/detail';
        var m = 'GET';
        var tmp_data = {'id' : data['questionId'][i]};
        $t(url, m, tmp_data, ques_get_succ, ques_get_fail, {which : window.contest.period_counter - 1});
    }
    console.log(info.contest.period[window.contest.period_counter - 1].question_id);
}

var per_get_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function period_bigger(a, b) {
    return a.lid > b.lid;
}

var org_get_succ = function(response) {
    var data = response.data;
    var start_time = new Date(data['signUpStart'] * 1000);
    var end_time = new Date(data['signUpEnd'] * 1000);
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
            case 'maxteam' :
                window.contest.attr[i].content = data['maxTeamMembers'].toString();
                break;
            case 'c_file' :
                window.contest.attr[i].content = data['signUpAttachmentUrl'];
                break;
        }
    }
    window.contest.period_counter = 0;
    window.contest.period_id = data['periods'];
    window.contest.period = []
    for (i in data['periods']) {
        var url = '/api/o/period/detail';
        var m = 'GET';
        var data = {'id' : data['periods'][i]};
        $t(url, m, data, per_get_succ, per_get_fail);
    }
    window.contest['period'].sort(period_bigger);
    for (i in window.contest['period']) {
        window.contest['period'].lid = i.toString();
    }
    //logoUrl bannerUrl level currentTime tags
    init_header();
    init_contest();
};

var org_get_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
};


var org_get_contest_detail = function() {
    var url = '/api/o/contest/detail';
    var m = 'GET';
    var data = {'id' : window.cid};
    $t(url, m, data, org_get_succ, org_get_fail);
    //url = '/api/o/contest/team_batch_manage';
    //$t(url, m, data, player_get_succ, player_get_fail);
};

(function () {
    //PLAYER = 0, ORGANIZER = 1
    $t('/api/c/user_type', 'GET', {},
        function (response) {
            usertype = response['data'];
            if (usertype == type_o) {
                org_get_contest_detail();
            }
            if (usertype == type_p) {
            }
        },
        function (response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    );
})();

var init_header = function() {
    header.greeting = contest != null ? contest.getAttr('name') : 'Test.Me';
    header.title = '比赛管理';
    header.link_list.push({
        alias : '比赛论坛',
        link : '../forum/index.html?cid=' + window.cid,
        action : empty_f
    });
    header.link_list.push({
        alias : '个人中心',
        link : '../myaccount/index.html',
        action : empty_f
    });
    header.link_list.push({
        alias : '登出',
        link : '#',
        action : function() {
            logout();
        }
    });
    nav.list = ['比赛信息', '申诉处理', '选手管理', '成绩录入'];
    nav.choice = '比赛信息';
}

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

var c_upload_pass = function(response) {
    for (i of info.contest.attr)
        if (i.name == 'c_file')
            i.content = response.data;
}

var c_upload_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var p_upload_pass = function(response, param) {
    var aim = param['aim'];
    for (i of this.contest.period)
        if ('p' + i.lid == aim)
            for (j of i.attr)
                if (j.name == 'p_file')
                     j.content = response.data;
}

var p_upload_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var q_upload_pass = function(response, param) {
    var aim = param['aim'];
    for (i of this.contest.period)
        for (j of i.question)
            if ('q' + j.lid + '-' + (parseInt(i.lid) + 1).toString() == aim)
                for (k of j.attr)
                    if (k.name == 'q_file')
                        k.content = response.data;
}

var q_upload_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}



var init_contest = function () {
info = new Vue({
    el : '#body',
    data : {
        show_basic_info : true,
        show_period_info : true,
        contest : window.contest,
        result_file_name : 'hahahah',
        upload_result_avail : true
    },
    computed : {
        is_guest : function() {
            return contest.is_guest;
        },
        is_organizer : function() {
            return usertype == type_o;
        },
        page : function() {
            return nav.choice;
        }
    },
    methods : {
        switch_basic_info : function() {
            this.show_basic_info = !this.show_basic_info;
        },
        c_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'contest_attachment');
            $t(url, m, data, c_upload_pass, c_upload_fail);
        },
        switch_period_info : function() {
            this.show_period_info = !this.show_period_info;
        },
        p_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'period_attachment');
            $t(url, m, data, p_upload_pass, p_upload_fail, {'aim' : e.target.id});
        },
        q_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            for (i of this.contest.period)
                for (j of i.question)
                    if ('q' + j.lid + '-' + (parseInt(i.lid) + 1).toString() == e.target.id)
                        for (k of j.attr)
                            if (k.name == 'q_file')
                                k.content = files[0].name;
                                //api
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'period_attachment');
            $t(url, m, data, q_upload_pass, q_upload_fail, {'aim' : e.target.id});
        },
        remove_period : function(idx) {
            if ((idx >= this.contest.period.length) || (idx < 0)) {
                console.log('[err] No such element');
                return;
            }
            this.contest.period.splice(idx, 1);
            //API
        },
        insert_new_period : function() {
            var new_period = {
                lid : this.contest.period_counter.toString(),
                attr : [
                    {
                        name : 'name',
                        alias : '阶段名称',
                        type : 'text',
                        content : '阶段 ' + this.contest.period_counter.toString(),
                        editable : true
                    },
                    {
                        name : 'description',
                        alias : '阶段简介',
                        type : 'ltext',
                        content : '简介',
                        editable : true
                    },
                    {
                        name : 'time',
                        alias : '阶段时间',
                        type : 'datetime',
                        content : {
                            sd : '',
                            ed : '',
                            sh : '',
                            sm : '',
                            eh : '',
                            em : ''
                        },
                        editable : true
                    },
                    {
                        name : 'slots',
                        alias : '可参与团队数',
                        type : 'number',
                        content : '',
                        editable : true
                    },
                    {
                        name : 'p_file',
                        alias : '阶段附件',
                        editable : true,
                        type : 'file',
                        content : ''
                    }
                ],
                question_modifier_available : true,
                question_counter : 0,
                question_id : [],
                question : [],
            };
            this.contest.period.push(new_period);
            ++this.contest.period_counter;
        },
        get_p_name : function(idx) {
            for (i of this.contest.period[idx].attr)
                if (i.name == 'name')
                    return(i.content);
        },
        remove_period : function(idx) {
            if ((idx >= this.contest.period.length) || (idx < 0)) {
                console.log('[err] No such element');
                return;
            }
            this.contest.period.splice(idx, 1);
        },
        insert_new_question : function(pidx) {
            var new_question = {
                lid : this.contest.period[pidx].question_counter.toString(),
                attr : [
                    {
                        name : 'description',
                        alias : '题目描述',
                        type : 'ltext',
                        editable : true,
                        content : ''
                    },
                    {
                        name : 'slots',
                        alias : '提交次数上限',
                        type : 'number',
                        editable : true,
                        content : ''
                    },
                    {
                        name : 'q_file',
                        alias : '题目附件',
                        type : 'file',
                        editable : true,
                        content : ''
                    }
                ],
            };
            ++this.contest.period[pidx].question_counter;
            this.contest.period[pidx].question.push(new_question);
        },
        remove_question : function(pidx, qidx) {
            if ((pidx >= this.contest.period.length || pidx < 0) || (qidx >= this.contest.period[pidx].question.length || qidx < 0)) {
                console.log('[err] No such item');
                return;
            }
            this.contest.period[pidx].question.splice(qidx, 1);
        },
        publish : function() {
            upload_data(0);
        },
        save : function() {
            upload_data(1);
        }
    }
});
}

var q_post_succ = function (response, param) {
    var n = param.which;
    info.contest.period[n].question_id.push(response.data);
}

var post_succ = function(response) {
    alert('修改成功！');
    window.location.assign('./index.html?cid=' + window.cid);
}

var post_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

var upload_data = function(aim_status) {
    for (i in info.contest.period_id) {
        var url = '/api/o/period/remove';
        var m = 'POST';
        var data = {id : info.contest.period_id[i]};
        $t(url, m, data, function() {}, function(response) {alert('[' + response.code.toString() + ']' + response.msg);});
    }
    for (i in info.contest.period) {
        /*for (j in info.contest.period[i].question_id) {
            var url = '/api/o/question/remove';
            var m = 'POST';
            console.log(j, info.contest.period[i].question_id, info.contest.period[i].question_id[j])
            var data = {id : info.contest.period[i].question_id[j]};
            $t(url, m, data, function() {}, function(response) {alert('[' + response.code.toString() + ']' + response.msg);});
        }*/
        /*
        info.contest.period[i].question_id = [];
        var url = '/api/o/period/create';
        var m = 'POST';
        var data = {
            'id' : window.cid,
            'index' : i
        };
        for (k of info.contest.period[i].attr) {
            switch (k.name) {
                case 'name' :
                    data['name'] = k.content;
                    break;
                case 'description' :
                    data['description'] = k.content;
                    break;
                case 'slots' :
                    data['availableSlots'] = k.content;
                    break;
                case 'p_file':
                    data['attachmentUrl'] = k.content;
                    break;
                case 'time':
                    data['startTime'] = k.content['sd'] + ' ' + k.content['sh'] + ':' + k.content['sm'] + ':00';
                    data['endTime'] = k.content['ed'] + ' ' + k.content['eh'] + ':' + k.content['em'] + ':00';
                    break;
            }
        }
        $t(url, m, data, function(response, param) {
                var n = param.which;
                var id = response.data;
                info.contest.period_id[n] = id;
                for (j in info.contest.period[n].question) {
                    var url = '/api/o/question/create';
                    var m = 'POST';
                    var data = {'index' : j, 'periodId' : id};
                    for (k of info.contest.period[n].question[j].attr) {
                        switch (k.name) {
                            case 'description':
                                data['description'] = k.content;
                                break;
                            case 'slots':
                                data['submissionLimit'] = k.content;
                                break;
                            case 'q_file':
                                data['attachmentUrl'] = k.content;
                                break;
                        }
                    }
                    $t(url, m, data, q_post_succ, function(response) {alert('[' + response.code.toString() + ']' + response.msg);}, {which : n});
                }
            },
            function(response) {
                alert('[' + response.code.toString() + ']' + response.msg);
            },
            {which : i}
        );
    }
    //        self.check_input('id', , 'logoUrl', 'bannerUrl',
    //                      'level', 'tags')
    var url = '/api/o/contest/detail';
    var m = 'POST';
    var data = {'level' : 1, 'tags' : '', 'logoUrl' : '', 'bannerUrl' : '', 'id' : window.cid};
    for (i of info.contest.attr) {
        switch (i.name) {
            case 'name' :
                data['name'] = i.content;
                break;
            case 'description' :
                data['description'] = i.content;
                break;
            case 'time' :
                data['signUpStart'] = i.content['sd'] + ' ' + i.content['sh'] + ':' + i.content['sm'] + ':00';
                data['signUpEnd'] = i.content['ed'] + ' ' + i.content['eh'] + ':' + i.content['em'] + ':00';
                break;
            case 'maxteam' :
                data['maxTeamMembers'] = i.content;
                break;
            case 'slots' :
                data['availableSlots'] = i.content;
                break;
            case 'c_file' :
                data['signUpAttachmentUrl'] = i.content;
        }
    }
    $t(url, m, data, post_succ, post_fail);
}
*/

// for develop without API

window.contest = {
    getAttr : function(qname) {
        for (i of this.attr)
            if (i.name == qname)
                return i.content;
        console.log('[err] No such attr');
        return null;
    },
    period_counter : 1,
    period_id : [],
    period : [],
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
            content : 'description 1',
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
            name : 'maxteam',
            alias : '团队人数上限',
            type : 'number',
            content : '100',
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
            name : 'processed',
            alias : '已审核',
            type : 'progress',
            content : {
                base : 'slots',
                value : '100'
            },
            editable : true
        },
        {
            name : 'c_file',
            alias : '比赛附件',
            type : 'file',
            content : ''
        }
    ],
    is_guest : false,
    period_modifier_available : true
};

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
});

header.greeting = contest != null ? contest.getAttr('name') : 'Test.Me';
header.title = '比赛';
header.title += '管理';

header.link_list.push({
    alias : '比赛论坛',
    link : '../forum/index.html?cid=' + window.cid,
    action : empty_f
    });
    header.link_list.push({
        alias : '个人中心',
        link : '../myaccount/index.html',
        action : empty_f
    });
    header.link_list.push({
        alias : '登出',
        link : '#',
        action : function() {
            logout();
        }
    });
header.link_list.push({
    alias : '登录',
    link : '../index.html',
    action : empty_f
});
nav.list = ['比赛信息', '申诉处理', '选手管理', '成绩录入'];
nav.choice = '比赛信息';

info = new Vue({
    el : '#body',
    data : {
        show_basic_info : true,
        show_period_info : true,
        show_upload_toknow : true,
        contest : window.contest,
        result_file_name : 'hahahah',
        upload_result_avail : true,
        appeal_list : [
            [
                {
                    appealer : {
                        name : '405',
                        id : '1'
                    },
                    type : 'score',
                    status : 'to process',
                    title : 'fuck zyn',
                    content : 'fuckkkkkkkkkk zyn',
                    a_url : '#',
                    selected : false
                },
                {
                    appealer : {
                        name : '405',
                        id : '1'
                    },
                    type : 'critirea',
                    status : 'processed',
                    title : 'fuck zyn',
                    content : 'fuckkkkkkkkkk zyn',
                    a_url : '#',
                    selected : false
                }
            ],
            [
                {
                    appealer : {
                        name : '405',
                        id : '1'
                    },
                    type : 'score',
                    status : 'ignored',
                    title : 'fuck zyn too',
                    content : 'fuckkkkkkkkkk zyn',
                    a_url : '#',
                    selected : false
                }
            ]
        ],
        appeal_page : 0,
        selected_appeal : 0
    },
    computed : {
        is_guest : function() {
            return contest.is_guest;
        },
        is_organizer : function() {
            return usertype == type_o;
        },
        page : function() {
            return nav.choice;
        },
        last_period_name : function() {
            for (a of this.contest.period[0].attr)
                if (a.name == 'name')
                    return a.content;
            alert('No valid period');
            return('wow');
        }
    },
    methods : {
        switch_basic_info : function() {
            this.show_basic_info = !this.show_basic_info;
        },
        switch_upload_toknow : function() {
            this.show_upload_toknow = !this.show_upload_toknow;
        },
        c_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
        },
        switch_period_info : function() {
            this.show_period_info = !this.show_period_info;
        },
        p_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
        },
        q_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            for (i of this.contest.period)
                for (j of i.question)
                    if ('q' + j.lid + '-' + (parseInt(i.lid) + 1).toString() == e.target.id)
                        for (k of j.attr)
                            if (k.name == 'q_file')
                                k.content = files[0].name;
        },
        r_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.result_file_name = files[0].name;
        },
        insert_new_period : function() {
            var new_period = {
                lid : this.contest.period_counter.toString(),
                attr : [
                    {
                        name : 'name',
                        alias : '阶段名称',
                        type : 'text',
                        content : '阶段 ' + this.contest.period_counter.toString(),
                        editable : true
                    },
                    {
                        name : 'description',
                        alias : '阶段简介',
                        type : 'ltext',
                        content : '简介',
                        editable : true
                    },
                    {
                        name : 'time',
                        alias : '阶段时间',
                        type : 'datetime',
                        content : {
                            sd : '',
                            ed : '',
                            sh : '',
                            sm : '',
                            eh : '',
                            em : ''
                        },
                        editable : true
                    },
                    {
                        name : 'slots',
                        alias : '可参与团队数',
                        type : 'number',
                        content : '',
                        editable : true
                    },
                    {
                        name : 'p_file',
                        alias : '阶段附件',
                        editable : true,
                        type : 'file',
                        content : ''
                    }
                ],
                question_modifier_available : true,
                question_counter : 0,
                question_id : [],
                question : [],
            };
            this.contest.period.push(new_period);
            ++this.contest.period_counter;
        },
        get_p_name : function(idx) {
            for (i of this.contest.period[idx].attr)
                if (i.name == 'name')
                    return(i.content);
        },
        remove_period : function(idx) {
            if ((idx >= this.contest.period.length) || (idx < 0)) {
                console.log('[err] No such element');
                return;
            }
            this.contest.period.splice(idx, 1);
        },
        insert_new_question : function(pidx) {
            var new_question = {
                lid : this.contest.period[pidx].question_counter.toString(),
                attr : [
                    {
                        name : 'description',
                        alias : '题目描述',
                        type : 'ltext',
                        editable : true,
                        content : ''
                    },
                    {
                        name : 'slots',
                        alias : '提交次数上限',
                        type : 'number',
                        editable : true,
                        content : ''
                    },
                    {
                        name : 'q_file',
                        alias : '题目附件',
                        type : 'file',
                        editable : true,
                        content : ''
                    }
                ],
            };
            ++this.contest.period[pidx].question_counter;
            this.contest.period[pidx].question.push(new_question);
        },
        remove_question : function(pidx, qidx) {
            if ((pidx >= this.contest.period.length || pidx < 0) || (qidx >= this.contest.period[pidx].question.length || qidx < 0)) {
                console.log('[err] No such item');
                return;
            }
            this.contest.period[pidx].question.splice(qidx, 1);
        },
        prev_a_page : function() {
            --this.appeal_page;
            if (this.appeal_page < 0)
                this.appeal_page = 0;
        },
        next_a_page : function() {
            ++this.appeal_page;
            if (this.appeal_page == this.appeal_list.length)
                this.appeal_page = this.appeal_list.length - 1;
        },
        select_appeal : function(page, idx) {
            this.appeal_list[page][idx].selected = !this.appeal_list[page][idx].selected;
            if (this.appeal_list[page][idx].selected)
                ++this.selected_appeal;
            else
                --this.selected_appeal;
        },
        select_page_appeal : function() {
            for (item of this.appeal_list[this.appeal_page]) {
                if (!item.selected)
                    ++this.selected_appeal;
                item.selected = true;
            }
        },
        unselect_page_appeal : function() {
            for (item of this.appeal_list[this.appeal_page]) {
                if (item.selected)
                    --this.selected_appeal;
                item.selected = false;
            }
        },
        select_all_appeal : function() {
            for (list of this.appeal_list) {
                for (item of list) {
                    if (!item.selected)
                        ++this.selected_appeal;
                    item.selected = true;
                }
            }
        },
        unselect_all_appeal : function() {
            for (list of this.appeal_list)
                for (item of list)
                    item.selected = false;
            this.selected_appeal = 0;
        },
        publish : function() {
        },
        save : function() {
        }
    }
});