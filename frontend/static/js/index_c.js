const type_p = 0;
const type_o = 1;

window.usertype = type_p;

var init_header = function() {
    header.greeting = 'Test.Me';
    header.title = '比赛大厅';

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
};

var test_item = {
    name : 'Contest1',
    organizer : '405',
    signuptimefrom : '2017-12-30',
    signuptimeto : '2017-12-31',
    contesttimefrom : '2017-12-31',
    contesttimeto : '2018-01-01',
    logo : '../img/user.png',
    url : '#'
}

var test_item2 = {
    name : 'Contest2',
    organizer : '405',
    signuptimefrom : '2017-12-30',
    signuptimeto : '2017-12-31',
    contesttimefrom : '2017-12-31',
    contesttimeto : '2018-01-01',
    logo : '../img/user.png',
    url : '#'
}



init_header();

var search_list = [
];

var controller = new Vue({
    el : '#body',
    data : {
        querytext : '',
        querylist : search_list,
        user : window.user,
        no_viewport : false,
        rec : []
    },
    computed : {
        user_type : function() {
            return window.usertype;
        }
    },
    methods : {
        searchcontest : function() {
            console.log("you're querying contest " + this.querytext);
            this.no_viewport = true;

        },
        next_rec : function() {
            for (item of this.rec)
                if (item.show) {
                    var ind = this.rec.indexOf(item);
                    ++ind;
                    ind %= this.rec.length;
                    item.show = false;
                    this.rec[ind].show = true;
                    return;
                }
            console.log('[err] Viewport is not initialized');
        }
    }
});

(function () {
    // get recommeded contests' banner list
    controller.rec.push({
        url : '../img/test1.jpg',
        show : false
    });
    controller.rec.push({
        url : '../img/test2.jpeg',
        show : false
    });

    // initialize viewport
    controller.rec[0].show = true;
    setInterval(controller.next_rec, 5000);
})();
