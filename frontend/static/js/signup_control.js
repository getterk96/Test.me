header_c.showsearchbox = false;
header_c.shownav = false;
header_c.link_list.push({
    alias : '登录',
    link : '../index.html',
});

var signup_c = new Vue({
    el : '#signup',
    data : {
        read : false,
        read_before_signup : [
            '1.因为涉及到真实身份的验证，请您填写真实信息，并妥善保管账号密码，避免个人信息泄露。',
            '2.待补充',
            '最后，TestU小组对以上条款有最终解释权。'],
        val_url : '',
        student_school : '',
        val_filename : '',
        tofill : [
            {
                label : '用户名',
                required : '',
                name : 'username',
                type : 'input',
                content : ''
            },
            {
                label : '密码',
                required : '',
                name : 'password',
                type : 'input',
                content : ''
            },
            {
                label : '电子邮件',
                required : '',
                name : 'email',
                type : 'input',
                content : ''
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
                label : '学校',
                required : '学生',
                name : 'school',
                type : 'input',
                content : ''
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
                type : 'time',
                content : {
                    y : '',
                    m : '',
                    d : ''
                }
            },
            {
                label : '组织名',
                required : '比赛主办方',
                name : 'organization',
                type : 'input',
                content : ''
            },
        ]
    },
    methods : {
        readthis : function () {
            this.read = true;
        },
        signup : function() {
            //fill api info below
            //api part please get file from the function 'val_file_change'
            //and check the functions 'signup_pass' and 'signup_fail'
            var url = '';
            var m = 'POST';
            var data = {'playerType' : 1};
            for (i in this.tofill) {
                if (this.tofill[i].name == 'usertype') {
                    if (this.tofill[i].choices.indexOf(this.usertype) == 0) {
                        url = 'api/p/register';
                    }
                    else if (this.tofill[i].choices.indexOf(this.usertype) == 1) {
                        url = 'api/o/register';
                    }
                    else {
                        alert('Wrong user type!');
                        return;
                    }
                }
                else if (this.tofill[i].name == 'school' && this.usertype == '学生') {
                    data['group'] = this.tofill[i].content;
                    console.log(this.tofill[i].content);
                }
                else if (this.tofill[i].name == 'organization' && this.usertype == '比赛主办方') {
                    data['group'] = this.tofill[i].content;
                }
                else if (this.tofill[i].name == 'gender' && this.usertype == '学生') {
                    if (this.tofill[i].choice == '男') {
                        data['gender'] = 'male';
                    }
                    else if (this.tofill[i].choice == '女') {
                        data['gender'] = 'female';
                    }
                    else {
                        alert('Wrong gender type!');
                        return;
                    }
                }
                else if (this.tofill[i].name == 'birthday' && this.usertype == '学生') {
                    data['birthday'] = this.tofill[i].content.y + '-' + this.tofill[i].content.m + '-' + this.tofill[i].content.d;
                }
                else {
                    data[this.tofill[i].name] = this.tofill[i].content;
                }
            }
            if (this.usertype == '比赛主办方') {
                data['verifyFileUrl'] = val_url;
            }
            $t(url, m, data, this.signup_pass, this.signup_fail);
        },
        selectusertype : function(choice) {
            for (i in this.tofill) {
                if (this.tofill[i].name == 'usertype') {
                    if (this.tofill[i].choices.indexOf(choice) != -1) {
                        this.tofill[i].choice = choice;
                        this.usertype = choice;
                    } else
                        console.log('[err] no such type');
                    break;
                }
            }
        },
        selectgender : function(choice) {
            for (i in this.tofill) {
                if (this.tofill[i].name == 'gender') {
                    if (this.tofill[i].choices.indexOf(choice) != -1)
                        this.tofill[i].choice = choice;
                    else
                        console.log('[err] no such type');
                    break;
                }
            }
        },
        val_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            console.log(files[0]);
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
        }

    },
    computed : {
        user_type : function() {
            for (i in this.tofill)
                if (this.tofill[i].name == 'usertype')
                    return this.tofill[i].choice;
            return '[none]';
        }
    }
})
