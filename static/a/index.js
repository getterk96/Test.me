var login_succ = function(response) {
    window.location.assign('backend.html');
}

var login_fail = function(response) {
    alert('[' + response.code + ']' + response.msg);
}

var ctrl = new Vue({
    el : '#login',
    data : {
        username : '',
        password : ''
    },
    methods : {
        login : function() {
            var url = '/api/c/login';
            var m = 'POST';
            var data = {
                username : this.username,
                password : this.password
            };
            $t(url, m, data, login_succ, login_fail);
        }
    }
});
