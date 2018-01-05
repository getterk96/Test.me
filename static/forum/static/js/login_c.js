var vp_bg = new Vue({
    el : '#viewport',
    data : {
        // r : recommended list
        r : []
    },
    methods : {
        next : function() {
            for (item of this.r)
                if (item.show) {
                    var ind = this.r.indexOf(item);
                    ++ind;
                    ind %= this.r.length;
                    item.show = false;
                    this.r[ind].show = true;
                    return;
                }
            console.log('[err] Viewport is not initialized');
        }
    }
});

var login = new Vue({
    el : '#login-box',
    data : {
        show_warning : false,
        warning : '',
        username : '',
        password : '',
        f : true
    },
    methods : {
        sendlogin : function(e) {
            if (e.keyCode == 13)
                this.login();
        },
        login : function() {
            if ((this.username == '') || (this.password == '')) {
                this.show_warning = true;
                this.warning = '用户名与密码不可为空!';
            } else {
                var url = '/api/c/login';
                var m = 'POST';
                var data = {};
                data['username'] = this.username;
                data['password'] = this.password;
                $t(url, m, data, this.login_pass, this.login_fail);
            }
        },
        login_pass : function() {
            window.location.assign('myaccount/index.html');
        },
        login_fail : function(response) {
            this.username = '';
            this.password = '';
            this.warning = response.msg;
        }
    },
    computed : {
        username_empty : function() {
            return this.username == '';
        }
    },
    directives : {
        focus : {
            update : function(el, {value}) {
                if (value)
                    el.focus();
            }
        }
    }
});

// viewport config
(function () {
    // get recommeded contests' banner list
    vp_bg.r.push({
        url : 'img/test1.jpg',
        show : false
    });
    vp_bg.r.push({
        url : 'img/test2.jpeg',
        show : false
    });

    // initialize viewport
    vp_bg.r[0].show = true;
    setInterval(vp_bg.next, 5000);
})();
