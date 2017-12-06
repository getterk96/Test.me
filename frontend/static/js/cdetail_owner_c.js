window.cid = window.get_args('cid');

window.usertype = 0;

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

//api

window.contest = {
    getAttr : function(qname) {
        for (i of this.attr)
            if (i.name == qname)
                return i.content;
        console.log('[err] No such attr');
        return null;
    },
    period_counter : 1,
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
            question_modifier_available : true,
            question_counter : 1,
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
    period_modifier_available : true
};

/*
window.user_id = '1'

window.team = {
    name : '405A',
    member : [
        {
            nickname : 'icariluci',
            avatar_url : '../img/user.png',
            school : 'THU',
            id : '1'
        },
        {
            nickname : 'irisangela',
            avatar_url : '../img/user.png',
            school : 'THU',
            id : '2'
        }
    ],
    leader_id : '1',
    new_leader : ''
}*/

/*
window.contest =  {
    getAttr : function(qname) {
        for (i of this.attr)
            if (i.name == qname)
                return i.content;
        console.log('[err] No such attr');
        return null;
    },
    attr : [
        {
            name : 'name',
            alias : '比赛名称',
            type : 'text',
            content : 'TI8'
        },
        {
            name : 'description',
            alias : '比赛简介',
            type : 'ltext',
            content : "The monks of Turstarkuri watched the rugged valleys below their mountain monastery as wave after wave of invaders swept through the lower kingdoms. Ascetic and pragmatic, in their remote monastic eyrie they remained aloof from mundane strife, wrapped in meditation that knew no gods or elements of magic. Then came the Legion of the Dead God, crusaders with a sinister mandate to replace all local worship with their Unliving Lord's poisonous nihilosophy. From a landscape that had known nothing but blood and battle for a thousand years, they tore the souls and bones of countless fallen legions and pitched them against Turstarkuri. The monastery stood scarcely a fortnight against the assault, and the few monks who bothered to surface from their meditations believed the invaders were but demonic visions sent to distract them from meditation. They died where they sat on their silken cushions. Only one youth survived--a pilgrim who had come as an acolyte, seeking wisdom, but had yet to be admitted to the monastery. He watched in horror as the monks to whom he had served tea and nettles were first slaughtered, then raised to join the ranks of the Dead God's priesthood. With nothing but a few of Turstarkuri's prized dogmatic scrolls, he crept away to the comparative safety of other lands, swearing to obliterate not only the Dead God's magic users--but to put an end to magic altogether."
        },
        {
            name : 'c_file',
            alias : '比赛附件',
            type : 'file',
            content : {
                url : '#',
                filename : 'description.pdf'
            }
        }
    ]
}
*/
header.greeting = contest != null ? contest.getAttr('name') : 'Test.Me';
header.title = '比赛管理';
/*
if  (!contest.is_guest && usertype == type_o)
    header.title += '管理';
else
    header.title += '详情';
*/
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
    });

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

nav.list = ['比赛信息', '申诉处理', '选手管理', '成绩录入'];
nav.choice = '比赛信息';
/*
} else if (!contest.is_guest && usertype == type_p) {
    nav.list = ['比赛信息','小队信息'];
    nav.choice = '比赛信息';
}*/

var info = new Vue({
    el : '#body',
    data : {
        show_basic_info : true,
        show_period_info : true,

        // for info page for participants
        //team : window.team,

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
        c_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            for (i of this.contest.attr)
                if (i.name == 'c_file')
                    i.content = files[0].name;
                    //api
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
                            //api
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
                question : []
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
                ]
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
            //api
        },
        save : function() {
            //api
        }
/*
        //for page of contest info for participants
        is_self : function(id) {
            for (i of team.member)
                if (i.id == id)
                    return user_id == id;
            console.log('[err] No such user');
            return false;
        },
        visit_user : function(id) {
            if (this.is_self(id)) {
                //visit myaccount
            } else {
                //guest visit
            }
        },
        switch_team_ownership : function() {
            //api
        }*/
    }
});
