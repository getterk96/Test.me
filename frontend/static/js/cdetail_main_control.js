header_c.showsearchbox = false;
header_c.link_list.push({
    alias : '登出',
    link : '#',
    action : function() {
        window.logout();
    }
});
header_c.nav_list.push({
    name : '比赛信息',
    link : '#',
    op : function() {
        header_c.change_nav_status();
        contest_c.page = 0;
    }
});
header_c.nav_list.push({
    name : '申诉处理',
    link : '#',
    op : function() {
        header_c.change_nav_status();
        contest_c.page = 1;
    }
});
header_c.nav_list.push({
    name : '选手管理',
    link : '#',
    op : function() {
        header_c.change_nav_status();
        contest_c.page = 2;
    }
});
header_c.nav_list.push({
    name : '成绩录入',
    link : '#',
    op : function() {
        header_c.change_nav_status();
        contest_c.page = 3;
    }
});

window.cid = window.get_args('cid');

//api part
window.contest = {
    name : {
        editable : true,
        content : 'hi'
    },
    description : {
        editable : true,
        content : 'oh'
    },
    time : {
        editable : true,
        content : {
            sy : '2017',
            sm : '11',
            sd : '21',
            sh : '19',
            sx : '00',
            ey : '2017',
            em : '11',
            ed : '21',
            eh : '20',
            ex : '00'
        }
    },
    slots : {
        editable : true,
        content : '100'
    },
    slots_filled : '50',
    attachment : {
        editable : true,
        filename : 'wow.pdf'
    },
    period_lock : false,
    period : [],
    period_id : [],
};
window.user = null;
window.playerlist = [
    {
        lid : 0,
        chosen : false,
        info : {
            'name' : 'ica',
            'status' : 'accepted',
            'rank' : '1'
        }
    },
    {
        lid : 1,
        chosen : false,
        info : {
            'name' : 'iris',
            'status' : 'accepted',
            'rank' : '-'
        }
    }
];

var setnav_header = function() {
    if (window.contest != null)
        header_c.nav_header = window.contest.name.content;
};
setnav_header();

window.query_player = function() {
    //api
    return {
        avatar_url : '../img/user.png'
    }
}

var contest_c = new Vue({
    el : '#contest-manager',
    data : {
        page : 0,
        contest : window.contest,

        usertype : -1,

        show_contest_basic_info : true,
        show_period_info : true,

        record_instruction : 'wow',
        rank_filename : '',

        playeronbatch : true,
        singleID : 0,
        single_player : null,
        playerlist : window.playerlist,
        sort_key : 'name',
        playerlistheader : [
            {
                name : 'name',
                alias : '选手名称'
            },
            {
                name : 'status',
                alias : '选手状态'
            },
            {
                name : 'rank',
                alias : '选手目前排名/分数'
            }
        ],
        key_dir : {
            'name' : true,
            'status' : true,
            'rank' : false
        }
    },
    methods : {
        change_basic_info : function() {
            this.show_contest_basic_info = !this.show_contest_basic_info;
        },
        contest_attachment_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.contest.attachment.filename = files[0].name;
        },
        change_period_info : function() {
            this.show_period_info = !this.show_period_info;
        },
        add_period : function() {
            var new_period = {
                id : 'p' + (window.contest.period.length + 1).toString(),
                name : {
                    editable : true,
                    content : 'period' + this.contest.period.length.toString()
                },
                description : {
                    editable : true,
                    content : 'description' + this.contest.period.length.toString()
                },
                time : {
                    editable : true,
                    content : {
                        sy : '-',
                        sm : '-',
                        sd : '-',
                        sh : '-',
                        sx : '-',
                        ey : '-',
                        em : '-',
                        ed : '-',
                        eh : '-',
                        ex : '-'
                    }
                },
                slots : {
                    editable : true,
                    content : '0'
                },
                slots_filled : '0',
                attachment : {
                    editable : true,
                    filename : '',
                    need_feed_back : 0,
                    change : function(e) {
                        var files = e.target.files || e.dataTransfer.files;
                        if (!files.length)
                            return;
                        for (item of window.contest.period) {
                            console.log(item.id, e.target.id);
                            if (item.id == e.target.id) {
                                item.attachment.filename = files[0].name;
                                item.attachment.need_feed_back = 1;
                                var url = '/api/c/upload';
                                var m = 'POST';
                                var data = new FormData();
                                data.append('file', files[0]);
                                data.append('destination', 'period_attachment');
                                $t(url, m, data, item.attachment.upload_pass, item.attachment.upload_fail);
                            }
                        }
                    },
                    upload_pass : function(response) {
                        for (item of window.contest.period) {
                            if (item.attachment.need_feed_back == 1) {
                                item.attachment.need_feed_bakc = 0;
                                item.attachment.filename = response.data;
                            }
                        }
                    },
                    upload_fail : function(response) {
                        alert('[' + response.code.toString() + ']' + response.msg);
                    }
                }
            };
            this.contest.period.push(new_period);
        },
        submitcontestinfo : function() {
            //api
            for (i in window.contest['period_id']) {
                $t('/api/o/period/remove', 'POST', {'id' : window.contest['period_id'][i]},
                    function(response) {},
                    function(response) {
                        alert('[' + response.code.toString() + ']' + response.msg);
                    }
                );
            }
            for (i in window.contest['period']) {
                var url = '/api/o/period/create';
                var m = 'POST';
                var p = window.contest['period'][i];
                var t = p['time'].content;
                var data = {
                    'id' : window.cid,
                    'index' : i,
                    'name' : p['name'].content,
                    'description' : p['description'].content,
                    'startTime' : t.sy + '-' + t.sm + '-' + t.sd + ' ' + t.sh + ':' + t.sx + ':00',
                    'endTime' : t.ey + '-' + t.em + '-' + t.ed + ' ' + t.eh + ':' + t.ex + ':00',
                    'availableSlots' : p['slots'].content,
                    'attachmentUrl' : p['attachment'].filename,
                    'questionId' : []
                };
                $t(url, m, data,
                    function(response) {},
                    function(response) {
                        alert('[' + response.code.toString() + ']' + response.msg);
                    }
                );
            }
            var url = '/api/o/contest/detail';
            var m = 'POST';
            var t = window.contest['time'].content;
            var data = {
                'id' : window.cid,
                'name' : window.contest['name'].content,
                'status' : 1,
                'description' : window.contest['description'].content,
                'logoUrl' : '',
                'bannerUrl' : '',
                'signUpStart' : t.sy + '-' + t.sm + '-' + t.sd + ' ' + t.sh + ':' + t.sx + ':00',
                'signUpEnd' : t.ey + '-' + t.em + '-' + t.ed + ' ' + t.eh + ':' + t.ex + ':00',
                'availableSlots' : window.contest['slots'].content,
                'maxTeamMembers' : 3,
                'signUpAttachmentUrl' : window.contest['attachment'].filename,
                'level' : 1,
                'tags' : ''
            };
            $t(url, m, data, this.modify_succ, this.modify_fail);
        },
        modify_succ : function(response) {
            alert('Modify success!');
            window.location.assign('../myaccount/index.html');
        },
        modify_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        },
        rank_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.rank_filename = files[0].name;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'rank_file');
            $t(url, m, data, this.rank_upload_pass, this.rank_upload_fail);
        },
        rank_upload_pass : function(response) {
            this.rank_filename = response['data'];
            /*
            var url = '/api/o/batch_rank';
            var m = 'POST';
            var data = {
                'file' : this.rank_filename,
                'id' : window.cid
            }
            $t(url, m, data,
                function(response) {
                    alert('Ranking information modify sucess!');
                },
                function(response) {
                    alert('[' + response.code.toString() + ']' + response.msg);
                }
            );
            */
        },
        rank_upload_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        },
        change_sort_key : function(key) {
            for (i in playerlist) {
                var j = i - 1;
                var tmp = {};
                tmp.lid = playerlist[i].lid;
                tmp.info = {};
                for (header of this.playerlistheader) {
                    console.log(header.name);
                    tmp.info[header.name] = playerlist[i].info[header.name];
                }
                console.log(tmp);
                while (j >= 0) {
                    if ((this.playerlist[j + 1].info[key] < this.playerlist[j].info[key]) == !this.key_dir[key]) {
                        for (header of this.playerlistheader)
                            this.playerlist[j + 1].info[header.name] = this.playerlist[j].info[header.name];
                        --j;
                    }
                    break;
                }
                for (header of this.playerlistheader)
                    this.playerlist[j + 1].info[header.name] = tmp.info[header.name];
                console.log(j + 1, this.playerlist[j + 1].info.name);
            }
            this.key_dir[key] = !this.key_dir[key];
            this.sort_key = key;
        },
        change_player_chosen_status : function(lid_q) {
            for (i in this.playerlist)
                if (this.playerlist[i].lid == lid_q) {
                    this.playerlist[i].chosen = !this.playerlist[i].chosen;
                    return;
                }
        },
        set_all_player_status : function(value) {
            for (i in this.playerlist)
                this.playerlist[i].chosen = value;
        },
        single_player_process : function(lid_q) {
            this.playeronbatch = false;
            this.singleID = lid_q;
            //api
            this.single_player = window.query_player();
        },
        batch_player_process : function() {
            this.playeronbatch = true;
        },
        succ_player : function() {
            var idx;
            for (i in this.playerlist)
                if (this.playerlist[i].lid == this.singleID) {
                    idx = i;
                    break;
                }
            idx = parseInt(idx);
            ++idx;
            idx %= this.playerlist.length;
            this.singleID = this.playerlist[idx].lid;
            //api
            this.single_player = window.query_player();
        },
        prev_player : function() {
            var idx;
            for (i in this.playerlist)
                if (this.playerlist[i].lid == this.singleID) {
                    idx = i;
                    break;
                }
            idx = parseInt(idx);
            idx += this.playerlist.length;
            --idx;
            idx %= this.playerlist.length;
            this.singleID = this.playerlist[idx].lid;
            //api
            this.single_player = window.query_player();
        }
    },
    computed : {
        isorganizer : function() {
            return this.usertype == 1;
        },
        in_period : function() {
            //api part
            return  false;
        },
        in_contest : function() {
            //api part
            return true;
        },
        after_signup : function() {
            //api part
            return true;
        },
        before_all_period : function() {
            //api part
            return true;
        }
    }
});

var per_get_succ = function (response) {
    var data = response.data;
    var start_time = new Date(data['startTime'] * 1000);
    var end_time = new Date(data['endTime'] * 1000);
    var period = {
        id : 'p' + data['index'].toString(),
        index : data['index'],
        name : {
            editable : true,
            content : data['name']
        },
        description : {
            editable : true,
            content : data['description'],
        },
        time : {
            editable : true,
            content : {
                sy : start_time.getFullYear(),
                sm : start_time.getMonth() + 1,
                sd : start_time.getDate(),
                sh : start_time.getHours(),
                sx : start_time.getMinutes(),
                ey : end_time.getFullYear(),
                em : end_time.getMonth() + 1,
                ed : end_time.getDate(),
                eh : end_time.getHours(),
                ex : end_time.getMinutes()
            }
        },
        slots : {
            editable : true,
            content : data['availableSlots'].toString()
        },
        attachment : {
            editable : true,
            filename : data['attachmentUrl'],
            need_feed_back : 0,
            change : function(e) {
                var files = e.target.files || e.dataTransfer.files;
                if (!files.length)
                    return;
                for (item of window.contest.period) {
                     if (item.id == e.target.id) {
                         item.attachment.filename = files[0].name;
                         item.attachment.need_feed_back = 1;
                         var url = '/api/c/upload';
                         var m = 'POST';
                         var data = new FormData();
                         data.append('file', files[0]);
                         data.append('destination', 'period_attachment');
                         $t(url, m, data, item.attachment.upload_pass, item.attachment.upload_fail);
                     }
                }
            },
            upload_pass : function(response) {
                for (item of window.contest.period) {
                    if (item.attachment.need_feed_back == 1) {
                        item.attachment.need_feed_bakc = 0;
                        item.attachment.filename = response.data;
                    }
                }
            },
            upload_fail : function(response) {
                alert('[' + response.code.toString() + ']' + response.msg);
            }
        },
        question_id : data['questionId']
    }
    window.contest['period'].push(period);
}

var per_get_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
}

function bigger(a, b) {
    return a.index > b.index;
}

var org_get_succ = function(response) {
    var data = response.data;
    window.contest['name'].content = data['name'];
    window.contest['description'].content = data['name'];
    var start_time = new Date(data['signUpStart'] * 1000);
    var end_time = new Date(data['signUpEnd'] * 1000);
    window.contest['time'].content['sy'] = start_time.getFullYear();
    window.contest['time'].content['sm'] = start_time.getMonth() + 1;
    window.contest['time'].content['sd'] = start_time.getDate();
    window.contest['time'].content['sh'] = start_time.getHours();
    window.contest['time'].content['sx'] = start_time.getMinutes();
    window.contest['time'].content['ey'] = end_time.getFullYear();
    window.contest['time'].content['em'] = end_time.getMonth() + 1;
    window.contest['time'].content['ed'] = end_time.getDate();
    window.contest['time'].content['eh'] = end_time.getHours();
    window.contest['time'].content['ex'] = end_time.getMinutes();
    window.contest['slots'].content = data['availableSlots'].toString();
    window.contest['attachment'].filename = data['signUpAttachmentUrl'];
    window.contest['period_id'] = data['periods'];
    for (i in window.contest['period_id']) {
        var url = '/api/o/period/detail';
        var m = 'GET';
        var data = {'id' : window.contest['period_id'][i]};
        $t(url, m, data, per_get_succ, per_get_fail);
    }
    window.contest['period'].sort(bigger);
    //logoUrl bannerUrl level currentTime tags maxTeamMembers
};

var org_get_fail = function(response) {
    alert('[' + response.code.toString() + ']' + response.msg);
};

var org_get_contest_detail = function() {
    var url = '/api/o/contest/detail';
    var m = 'GET';
    var data = {'id' : window.cid};
    $t(url, m, data, org_get_succ, org_get_fail);
};

(function () {
    //PLAYER = 0, ORGANIZER = 1
    contest_c.usertype = -1;
    $t('/api/c/user_type', 'GET', {},
        function (response) {
            contest_c.usertype = response['data'];
            if (contest_c.usertype == 1) {
                org_get_contest_detail();
            }
        },
        function (response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    );
})();


