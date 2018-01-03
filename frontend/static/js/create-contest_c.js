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
    for (i in info.contest.period_id) {
        var url = '/api/o/period/remove';
        var m = 'POST';
        var data = {id : info.contest.period_id[i]};
        $t(url, m, data, function() {}, function(response) {alert('[' + response.code.toString() + ']' + response.msg);});
    }
    for (i in info.contest.period) {
        for (j in info.contest.period[i].question_id) {
            var url = '/api/o/question/remove';
            var m = 'POST';
            console.log(j, info.contest.period[i].question_id, info.contest.period[i].question_id[j])
            var data = {id : info.contest.period[i].question_id[j]};
            $t(url, m, data, function() {}, function(response) {alert('[' + response.code.toString() + ']' + response.msg);});
        }

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
                case 'pstime':
                    data['startTime'] = k.content['d'] + ' ' + k.content['h'] + ':' + k.content['m'] + ':00';
                    break;
                case 'petime':
                    data['endTime'] = k.content['d'] + ' ' + k.content['h'] + ':' + k.content['m'] + ':00';
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
            case 'signupstime' :
                data['signUpStart'] = i.content['d'] + ' ' + i.content['h'] + ':' + i.content['m'] + ':00';
                break;
            case 'signupetime' :
                data['signUpEnd'] = i.content['d'] + ' ' + i.content['h'] + ':' + i.content['m'] + ':00';
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
            name : 'signupstime',
            alias : '报名时间',
            type : 'datetime',
            content : {
                d : '1977-03-11',
                h : '19',
                m : '00'
            },
            editable : true
        },
        {
            name : 'signupetime',
            alias : '报名时间',
            type : 'datetime',
            content : {
                d : '1977-03-11',
                h : '19',
                m : '00'
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

var info = new Vue({
    el : '#body',
    data : {
        show_basic_info : true,
        show_period_info : true,
        contest : window.contest
    },
    computed : {},
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
        },
        quit : function() {
            var c = confirm('放弃本次的修改?')
            if (c == true) { window.location.assign('../myaccount/index.html'); }
        }
    }
});
