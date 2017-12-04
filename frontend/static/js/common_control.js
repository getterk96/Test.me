var dev_c = new Vue({
    el : '#dev-info',
    data : {
        version : '0.0',
        developer : 'Test U',
        project_name : 'Test.Me'
    },
    computed : {
        info : function () {
            return this.project_name + 'v' + this.version + ' developed by ' + this.developer;
        }
    }
})

window.userid = window.get_args('userid');

window.logout = function() {
    var url = '/api/c/logout';
    var m = 'POST';
    var data = {};
    $t(url, m, data, this.logout_proc, this.logout_fail);
};

window.logout_proc = function(response) {
	window.location.assign('../index.html');
};

window.logout_fail = function(response) {
	alert("登出失败！");
};

var header_c = new Vue({
    el : '#header',
    data : {
        showheader : true,
        shownav : true,
        showpersonal : true,
        showsearchbox : true,
        showsearchinput : false,
        display_nav : false,
        color : "color-themed",
        color_nav : 'color-themed-alpha',
        nav_header : 'Test.Me',
        nav_c : '>',
        nav_list : [],
        link_list : []
    },
    methods : {
        change_nav_status : function () {
            this.display_nav = !this.display_nav;
            if (this.display_nav)
                this.nav_c = '<';
            else
                this.nav_c = '>';
        },
        change_search_status : function() {
            this.showsearchinput = !this.showsearchinput;
        }
    }
})
