var redirect_c = new Vue({
    el : '#info-container',
    computed : {
        redirectto : function() {
            toparse = window.location.href;
            if (toparse.indexOf('redirect?=') >= 0) {
                ret = toparse.substring(toparse.indexOf('redirect?=') + 10);
                if (ret == '')
                    ret = 'index.html';
            }
            else
                ret = 'index.html';
            return ret;
        }
    }
})

header_c.showheader = false;
