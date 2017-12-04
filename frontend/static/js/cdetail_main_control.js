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
    period : []
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
                id : 'p' + this.contest.period.length.toString(),
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
                    change : function(e) {
                        var files = e.target.files || e.dataTransfer.files;
                        if (!files.length)
                            return;
                        for (item of contest_c.contest.period) {
                            if (item.id == e.target.id) {
                                item.attachment.filename = files[0].name;
                                //api
                            }
                        }
                    }
                }
            };
            this.contest.period.push(new_period);
        },
        submitcontestinfo : function() {
            //api
            alert('submit');
        },
        rank_file_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.rank_filename = files[0].name;
            //api
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
            //api part
            return true;
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
