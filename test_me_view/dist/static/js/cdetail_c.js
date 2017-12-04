window.cid = window.get_args('cid');

window.usertype = 1;

const type_p = 0;
const type_o = 1;

(function () {
    //PLAYER = 0, ORGANIZER = 1
    $t('/api/c/user_type', 'GET', {},
        function (response) {
            myaccount_c.usertype = response['data'];
        },
        function (response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    );
})();

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
            lid : '0',
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
                    content : ''
                }
            ],
            question : [
                {
                    lid : '0',
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
                    ]
                }
            ],
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
            name : 'minteam',
            alias : '团队人数下限',
            type : 'number',
            content : '100',
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
    is_guest : false
};

header.greeting = contest != null ? contest.getAttr('name') : 'Test.Me';
header.title = '比赛';
if  (!contest.is_guest && usertype == type_o)
    header.title += '管理';
else
    header.title += '详情';

if (usertype in [0, 1]) {
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
} else
    header.link_list.push({
        alias : '登录',
        link : '../index.html',
        action : empty_f
    })

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

if (!contest.is_guest && usertype == type_o) {
    nav.list = ['比赛信息', '申诉处理', '选手管理', '成绩录入'];
    nav.choice = '比赛信息';
}

var info = new Vue({
    el : '#body',
    data : {
        show_basic_info : true,
        show_period_info : true,
        contest : window.contest
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
            for (i of this.contest.attr)
                if (i.name == 'c_file')
                    i.content = files[0].name;
        },
        switch_period_info : function() {
            this.show_period_info = !this.show_period_info;
        },
        p_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            for (i of this.contest.period)
                if ('p' + i.lid == e.target.id)
                    for (j of i.attr)
                        if (j.name == 'p_file')
                            j.content = files[0].name;
        },
        q_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            for (i of this.contest.period)
                for (j of i.question)
                    if ('q' + i.lid + '-' + (parseInt(j.lid) + 1).toString() == e.target.id)
                        for (k of j.attr)
                            if (k.name == 'q_file')
                                k.content = files[0].name;
        }
    }
})
