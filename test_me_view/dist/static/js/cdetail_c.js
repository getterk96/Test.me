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
    attr : [
        {
            name : 'name',
            content : 'contest 1',
            editable : true
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
        list : ['比赛信息', '申诉处理', '选手管理', '成绩录入'],
        choice : '比赛信息'
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
