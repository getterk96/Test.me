var header = new Vue({
    el : '#header',
    data : {
        greeting : '',
        title : '',
        link_list : []
    }
})

header.link_list.push({
    alias : '比赛大厅',
    link : '../index/index.html',
    action : empty_f
});
