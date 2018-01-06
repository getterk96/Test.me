var creator_c = new Vue({
    el : '#contest-creator',
    data : {
        id : -1,
        isorganizer : true,
        show_contest_basic_info : true,
        show_period_info : true,
        contest : {
            name : '',
            description : '',
            time :  {
                sy : '',
                sm : '',
                sd : '',
                sh : '',
                sx : '',
                ey : '',
                em : '',
                ed : '',
                eh : '',
                ex : '',
            },
            slots : '',
            period : [],
            attachment : {
                filename : ''
            }
        }
    },
    methods : {
        change_basic_info : function() {
            this.show_contest_basic_info = !this.show_contest_basic_info;
        },
        change_period_info : function() {
            this.show_period_info = !this.show_period_info;
        },
        contest_attachment_change : function(e) {
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length)
                return;
            this.contest.attachment.filename = files[0].name;
            var url = '/api/c/upload';
            var m = 'POST';
            var data = new FormData();
            data.append('file', files[0]);
            data.append('destination', 'contest_attachment');
            $t(url, m, data, this.upload_pass, this.upload_fail);
        },
        upload_pass : function(response) {
            this.contest.attachment.filename = response.data;
        },
        upload_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        },
        add_period : function() {
            var new_period = {
                id : 'p' + this.contest.period.length.toString(),
                name : 'period' + this.contest.period.length.toString(),
                description : 'description' + this.contest.period.length.toString(),
                time : {
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
                },
                slots : '',
                attachment : {
                    filename : '',
                    need_feed_back : 0,
                    change : function(e) {
                        var files = e.target.files || e.dataTransfer.files;
                        if (!files.length)
                            return;
                        for (item of creator_c.contest.period) {
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
                        for (item of creator_c.contest.period) {
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
        create_contest : function() {
            var url = '/api/o/contest/create';
            var m = 'POST';
            var t = creator_c.contest.time;
            var data = {
                'tags' : '',
                'level' : 1,
                'logoUrl' : '',
                'bannerUrl' : '',
                'maxTeamMembers' : 3,
                'name' : creator_c.contest.name,
                'description' : creator_c.contest.description,
                'availableSlots' : creator_c.contest.slots,
                'signUpAttachmentUrl' : creator_c.contest.attachment.filename,
                'signUpStart' : t.sy + '-' + t.sm + '-' + t.sd + ' ' + t.sh + ':' + t.sx + ':00',
                'signUpEnd' : t.ey + '-' + t.em + '-' + t.ed + ' ' + t.eh + ':' + t.ex + ':00',
            };
            $t(url, m, data, this.create_pass, this.create_fail);
        },
        create_pass : function(response) {
            this.id = response.data;
            var url = 'api/o/period/create';
            var m = 'POST';
            for(i in this.contest.period) {
                var t = this.contest.period[i].time;
                var data = {
                    'id' : this.id,
                    'name' : this.contest.period[i].name,
                    'description' : this.contest.period[i].description,
                    'availableSlots' : this.contest.period[i].slots,
                    'attachmentUrl' : this.contest.period[i].attachment.filename,
                    'startTime' : t.sy + '-' + t.sm + '-' + t.sd + ' ' + t.sh + ':' + t.sx + ':00',
                    'endTime' : t.ey + '-' + t.em + '-' + t.ed + ' ' + t.eh + ':' + t.ex + ':00',
                    'index' : i,
                    'questionId' : [],
                };
                $t(url, m, data, this.period_create_pass, this.period_create_fail);
            }
            window.location.assign("../myaccount/index.html");
        },
        create_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        },
        period_create_pass : function(response) {
        },
        period_create_fail : function(response) {
            alert('[' + response.code.toString() + ']' + response.msg);
        }
    },
    computed : {
    }
})
