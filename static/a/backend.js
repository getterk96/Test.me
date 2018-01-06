var ctrl = new Vue({
    el : '#backend',
    data : {
        user_process : true,
        user_list : [],
        contest_list : [],
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
        accept_user : function() {},
        deny_user : function() {},
        switch_plat : function () {
            this.user_process = !this.user_process;
        },
        accept_contest : function(id) {
            //todo
        },
        deny_contest : function(id) {
            //todo
        }
    }
});

test_user = {
    name : 'wowo',
    description : 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    attachment : '#',
    status : 0,
    id : '1'
};

test_contest = {
    organizer : {
        name : 'sssss',
        id : '1'
    },
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
            content : 'niupi',
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
            name : 'stime',
            alias : '报名开始时间',
            type : 'datetime',
            content : {
                d : '1999-01-01',
                h : '1',
                m : '1'
            }
        },
        {
            name : 'etime',
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
