const type_p = 0;
const type_o = 1;

window.usertype = type_p;

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

var init_header = function() {
    header.greeting = 'Test.Me';
    header.title = '个人中心';

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
    if (usertype == type_p) {
        nav.list = ['比赛大厅', '个人信息', '我的比赛', '我的队伍'];
        nav.choice = '比赛大厅';
    }
};


init_header();

var search_list = [
    {
        name : 'contest1',
        organizer : 'THU',
        sut : '2017-7-30 to 2017-8-2',
        ct : '2017-8-15 to 2017-8-20',
        link : '#'
    },
    {
        name : 'contest2',
        organizer : 'PKU',
        sut : '2017-7-31 to 2017-8-3',
        ct : '2017-8-16 to 2017-8-21',
        link : '#'
    }
];

window.user = {
    avatar : {
        editable : true,
        link : "../img/default_avatar.jpg"
    }
}

var controller = new Vue({
  el : '#body',
  data : {
    querytext : '',
    querylist : search_list,
    user : window.user
  },
  computed : {
    page : function() {
      return nav.choice;
    }
  },
  methods : {
    clearsearchbox : function() {
      this.querytext = '';
    },
    searchcontest : function() {
        console.log("you're querying contest " + this.querytext);
    },
    randomcontest : function() {
        console.log("return a random contest");
    },
    uploadavatar : function(e) {
        var files = e.target.files || e.dataTransfer.files;
        if (!files.length)
            return;
        alert('succeed!')
    }
  }
})
