const type_p = 0;
const type_o = 1;

window.usertype = type_o;

var init_header = function() {
    header.greeting = 'Test.Me';
    header.title = '创建比赛';

    if (usertype == 1) {
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
    } else
        header.link_list.push({
            alias : '登录',
            link : '../index.html',
            action : empty_f
        })
};

init_header();


var upload_data = function(aim_status) {
    var url = '/api/o/contest/create';
    var m = 'POST';
    var data = {
        'tags' : ''
    };
    for (k of info.contest.attr) {
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
            case 'c_file':
                data['signUpAttachmentUrl'] = k.content;
                break;
            case 'signupstime':
                data['signUpStart'] = k.content['d'] + ' ' + k.content['h'] + ':' + k.content['m'] + ':00';
                break;
            case 'signupetime':
                data['signUpEnd'] = k.content['d'] + ' ' + k.content['h'] + ':' + k.content['m'] + ':00';
                break;
            case 'level':
                data['level'] = k.choices.indexOf(k.choice);
                break;
            case 'maxteam':
                data['maxTeamMembers'] = k.content;
                break;
            case 'c_logo':
                data['logoUrl'] = k.content;
                break;
            case 'c_banner':
                data['bannerUrl'] = k.content;
                break;
        }
    }
    $t(url, m, data, create_pass, create_fail);
}

var create_pass = function(response) {
    this.id = response.data;
    var url = 'api/o/period/create';
    var m = 'POST';
    for (i in info.contest.period) {
        var data = {
            'id' : this.id,
            'index' : i,
            'questionId' : []
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
                case 'pstime':
                    data['startTime'] = k.content['d'] + ' ' + k.content['h'] + ':' + k.content['m'] + ':00';
                    break;
                case 'petime':
                    data['endTime'] = k.content['d'] + ' ' + k.content['h'] + ':' + k.content['m'] + ':00';
                    break;
            }
        }
        $t(url, m, data, p_create_pass, p_create_fail);
    }
    window.location.assign('../myaccount/index.html');
}

var create_fail = function(response) { alert('[' + response.code.toString() + ']' + response.msg); };

var p_create_pass = function(response) {};

var p_create_fail = function(response) { alert('[' + response.code.toString() + ']' + response.msg); }

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
            content : '',
            editable : true
        },
        {
            name : 'description',
            alias : '比赛简介',
            type : 'ltext',
            content : '',
            editable : true
        },
        {
            name : 'level',
            alias : '比赛级别',
            type : 'radio',
            choice : '[none]',
            editable : true,
            choices : ['国际级', '国家级', '省级', '市级', '区级', '校级', '院系级']
        },
        {
            name : 'signupstime',
            alias : '报名时间',
            type : 'datetime',
            content : {
                d : '',
                h : '',
                m : ''
            },
            editable : true
        },
        {
            name : 'signupetime',
            alias : '报名时间',
            type : 'datetime',
            content : {
                d : '',
                h : '',
                m : ''
            },
            editable : true
        },
        {
            name : 'maxteam',
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
            content : ''
        },
        {
            name : 'c_logo',
            alias : '比赛logo',
            type : 'logo',
            content : ''
        },
        {
            name : 'c_banner',
            alias : '比赛横幅',
            type : 'banner',
            content : ''
        }
    ],
    period_modifier_available : true
};

var c_upload_pass = function(response) {
    for (i of info.contest.attr)
        if (i.name == 'c_file')
            i.content = response.data;
};

var c_upload_fail = function(response) { alert('[' + response.code.toString() + ']' + response.msg); };

var p_upload_pass = function(response, param) {
    var aim = param['aim'];
    for (i of this.contest.period)
        if ('p' + i.lid == aim)
            for (j of i.attr)
                if (j.name == 'p_file')
                     j.content = response.data;
};

var p_upload_fail = function(response) { alert('[' + response.code.toString() + ']' + response.msg); };

var logo_upload_pass = function(response) {
    for (i of info.contest.attr)
        if (i.name == 'c_logo')
            i.content = response.data;
};

var logo_upload_fail = function(response) { alert('[' + response.code.toString() + ']' + response.msg); };

var banner_upload_pass = function(response) {
    for (i of info.contest.attr)
        if (i.name == 'c_banner')
            i.content = response.data;
};

var banner_upload_fail = function(response) { alert('[' + response.code.toString() + ']' + response.msg); };

var info = new Vue({
    el : '#body',
    data : {
        show_basic_info : true,
        show_period_info : true,
        contest : window.contest
    },
    computed : {},
    methods : {
        switch_basic_info : function() { this.show_basic_info = !this.show_basic_info; },
        switch_period_info : function() { this.show_period_info = !this.show_period_info; },
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
        remove_period : function(idx) {
            if ((idx >= this.contest.period.length) || (idx < 0)) {
                console.log('[err] No such element');
                return;
            }
            this.contest.period.splice(idx, 1);
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
                        name : 'pstime',
                        alias : '阶段开始时间',
                        type : 'datetime',
                        content : {
                            d : '',
                            h : '',
                            m : ''
                        },
                        editable : true
                    },
                    {
                        name : 'petime',
                        alias : '阶段结束时间',
                        type : 'datetime',
                        content : {
                            d : '',
                            h : '',
                            m : ''
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
                ]
            };
            this.contest.period.push(new_period);
            ++this.contest.period_counter;
        },
        get_p_name : function(idx) {
            for (i of this.contest.period[idx].attr)
                if (i.name == 'name')
                    return(i.content);
        },
        publish : function() {
            upload_data();
        },
        quit : function() {
            var c = confirm('放弃本次的修改?')
            if (c == true) { window.location.assign('../myaccount/index.html'); }
        },
        select : function(name, choice) {
            var target = null;
            for (i of this.contest.attr)
                if (i.name == name)
                    target = i;
            if (target == null) {
                console.log('[err] No such info item');
                return;
            }
            var exists = false;
            for (i of target.choices)
                if (i ==  choice) {
                    exists = true;
                    break;
                }
            if (!exists) {
                console.log('[err] No such choice');
                return;
            }
            if (target.type == 'radio')
                target.choice = choice;
        },
        c_logo_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'contest_logo');
            $t(url, m, data, logo_upload_pass, logo_upload_fail);
        },
        c_banner_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'contest_banner');
            $t(url, m, data, banner_upload_pass, banner_upload_fail);
        }
        //
    }
});
