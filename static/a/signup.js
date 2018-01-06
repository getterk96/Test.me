var ctrl = new Vue({
    el : '#signup',
    data : {
        username : '',
        password : '',
        cpassword : '',
        valcode : ''
    },
    methods : {
        signup : function() {
            if (password != cpassword) {
                alert('两次密码不一致');
                return;
            }
            //todo
        }
    }
});
