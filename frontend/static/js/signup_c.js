header.greeting = 'Test.Me';
header.title = '注册';
header.link_list.push({
    alias : '登录',
    link : '../index.html',
});

var signup = new Vue({
    el : '#body',
    data : {
        read : false,
        read_before_signup : [
            '1.因为涉及到真实身份的验证，请您填写真实信息，并妥善保管账号密码，避免个人信息泄露。',
            '2.待补充',
            '最后，TestU小组对以上条款有最终解释权。'],
        val_filename : '请选择文件',
        userinfo : [
            {
                label : '用户名',
                required : '',
                name : 'username',
                type : 'input',
                content : '',
                warning : '用户名中只可包含数字、字母和下划线且不可以下划线开头'
            },
            {
                label : '密码',
                required : '',
                name : 'password',
                type : 'input',
                content : '',
                warning : '密码只可包含数字、字母和下划线，长度应在8-20位之间'
            },
            {
                label : '确认密码',
                required : '',
                name : 'cpassword',
                type : 'input',
                content : '',
                warning : '请保持两次密码输入一致'
            },
            {
                label : '电子邮件',
                required : '',
                name : 'email',
                type : 'input',
                content : '',
                warning : '请确保邮箱格式正确'
            },
            {
                label : '昵称',
                required : '',
                name : 'nickname',
                type : 'input',
                content : '',
                warning : '昵称是你显示给其他用户的名字'
            },
            {
                label : '用户类型',
                required : '',
                name : 'usertype',
                type : 'radio',
                choice : '[none]',
                choices : ['学生', '比赛主办方']
            },
            {
                label : '学生类型',
                name : 'studenttype',
                required : '学生',
                type : 'radio',
                choice : '[none]',
                choices : ['高中生', '本科生', '研究生', '专科生']
            },
            {
                label : '学校',
                required : '学生',
                name : 'school',
                type : 'input',
                content : '',
                warning : ''
            },
            {
                label : '性别',
                required : '学生',
                name : 'gender',
                type : 'radio',
                choice : '[none]',
                choices : ['男','女']
            },
            {
                label : '生日',
                required : '学生',
                name : 'birthday',
                type : 'date',
                content : '',
                warning : ''
            },
            {
                label : '组织名',
                required : '比赛主办方',
                name : 'organization',
                type : 'input',
                content : ''
            },
            {
                label : '验证文档',
                required : '比赛主办方',
                name : 'val_file',
                type : 'file'
            },
        ]
    },
    computed : {
        usertype : function() {
            for (i of this.userinfo)
                if (i.name == 'usertype')
                    return i.choice;
        }
    },
    methods : {
        read_this : function() {
            this.read = true;
        },
        select : function(item, choice) {
            var target = null;
            for (i of this.userinfo)
                if (i.name == item)
                    target = i;
            if (target == null) {
                console.log('[err] No such info item');
                return;
            }
            var exists = false;
            for (i of target.choices)
                if (i ==  choice) {
                    exists = true;
                    break;
                }
            if (!exists) {
                console.log('[err] No such choice');
                return;
            }
            if (target.type == 'radio')
                target.choice = choice;
        },
        val_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.val_filename = files[0].name;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'verification_file');
            $t(url, m, data, this.upload_pass, this.upload_fail);
        },
        signup_pass : function(response) {
            alert('注册成功！');
            window.location.assign('../index.html');
        },
        signup_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        },
        upload_pass : function(response) {
            val_url = response.data;
        },
        upload_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        },
        signup : function() {
            //fill api info below
            //api part please get file from the function 'val_file_change'
            //and check the functions 'signup_pass' and 'signup_fail'
            var url = '';
            var m = 'POST';
            var data = {'playerType' : 1};
            for (i in this.userinfo) {
                if (this.userinfo[i].name == 'usertype') {
                    if (this.userinfo[i].choices.indexOf(this.usertype) == 0) {
                        url = 'api/p/register';
                    }
                    else if (this.userinfo[i].choices.indexOf(this.usertype) == 1) {
                        url = 'api/o/register';
                    }
                    else {
                        alert('Wrong user type!');
                        return;
                    }
                }
                else if (this.userinfo[i].name == 'school' && this.usertype == '学生') {
                    data['group'] = this.userinfo[i].content;
                    console.log(this.userinfo[i].content);
                }
                else if (this.userinfo[i].name == 'organization' && this.usertype == '比赛主办方') {
                    data['group'] = this.userinfo[i].content;
                }
                else if (this.userinfo[i].name == 'gender' && this.usertype == '学生') {
                    if (this.userinfo[i].choice == '男') {
                        data['gender'] = 'male';
                    }
                    else if (this.userinfo[i].choice == '女') {
                        data['gender'] = 'female';
                    }
                    else {
                        alert('Wrong gender type!');
                        return;
                    }
                }
                else if (this.userinfo[i].name == 'birthday' && this.usertype == '学生') {
                    data['birthday'] = this.userinfo[i].content;
                }
                else {
                    data[this.userinfo[i].name] = this.userinfo[i].content;
                }
            }
            if (this.usertype == '比赛主办方') {
                data['verifyFileUrl'] = val_url;
            }
            $t(url, m, data, this.signup_pass, this.signup_fail);
        }
    }
})
