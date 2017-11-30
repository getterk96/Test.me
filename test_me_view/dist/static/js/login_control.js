var slogan_c = new Vue({
    el : '#slogan-box',
    data : { slogan : 'Test.Me, 挑战自我' }
})

var login_c = new Vue({
    el : '#login-box',
    data : {
        username : '',
        password : ''
    },
    methods : {
        log_in : function () {
            var url = '/api/c/login';
            var m = 'POST';
            var data = {};
            data['username'] = this.username;
            data['password'] = this.password;
            $t(url, m, data, this.login_pass, this.login_fail);
        },
        login_pass : function(response) {
            window.location.assign('myaccount/index.html');
        },
        login_fail : function(response) {
            this.username = '';
            this.password = '';
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    }
})

header_c.showheader = false;
