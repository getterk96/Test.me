var signup_succ = function(response) {
    window.location.assign('index.html');
};

var signup_fail = function(response) {
    alert('[' + response.code + ']' + response.msg);
}

var ctrl = new Vue({
    el : '#signup',
    data : {
        username : '',
        password : '',
        cpassword : '',
        valcode : ''
    },
    methods : {
        sendsignup : function(e) {
            if (e.keyCode == 13) { this.signup(); }
        },
        signup : function() {
            if (this.password != this.cpassword) {
                alert('两次密码不一致');
                return;
            }
            var url = "/api/a/register";
            var m = "POST";
            var data = {
                username : this.username,
                password : this.password,
                email : '',
                adminToken : this.valcode
            };
            $t(url, m, data, signup_succ, signup_fail);
        }
    }
});
