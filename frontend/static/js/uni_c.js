// universal controller
window.userid = window.get_args('userid');

window.logout = function() {
    var url = '/api/c/logout';
    var m = 'POST';
    var data = {};
    $t(url, m, data, this.logout_proc, this.logout_fail);
};

window.logout_proc = function(response) {
	window.location.assign('../index.html');
};

window.logout_fail = function(response) {
	alert("登出失败！");
};
