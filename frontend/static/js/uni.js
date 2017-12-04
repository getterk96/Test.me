// universal script
window.my_root_path = 'home/quincy/Work/test.me.view/'
axios.defaults.baseURL = 'http://127.0.0.1:8000';
axios.defaults.withCredentials = true;

// global methods
window.sendresp404 = function() {
    var path = window.my_root_path + '404.html?redirect=' + window.location.href;
    window.location.assign(path);
};

window.get_args = function(name) {
    var reg = new RegExp("(^|&)" + name + "=(([^&]*)(&|$))");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)
        return unescape(r[2]);
    return null;
};

window.empty_f = function() {};

//wrapped up request sender
(function(window, undefined) {
    // This wrapped-up request sender should be initialized with 5 arguments :
    // > the url requested
    // > the method of request with choices "POST" and "GET"
    // > the data to send
    //   > for "POST", the type of data should be 'FormData'
    //   > for "GET", the type of data should be a string
    // > the methods for response
    //   > proc for success response
    //   > exception for failure response
    //   > if no method should be referred, 'window.empty_f' can be used
    var _$t = window.$t;
    var _testme = window.testme;
    var testme = $t = window.$t = window.testme = function(url, method, data, proc, exception) {
        return new testme.prototype.init(url, method, data, proc, exception);
    }
    testme.fn = testme.prototype = {
        init : function(url, method, data, proc, exception) {
            if (typeof url == 'string') {
                if ((method != 'POST') && (method !='GET')) {
                    console.log('[err] invlalid method');
                    return undefined;
                }
                try {
                    data_str = JSON.stringify(data);
                } catch (e) {
                    console.log('[err] invalid json syntax');
                    return undefined
                }
                if ((typeof proc != 'function') || (typeof exception != 'function')) {
                    console.log('[err] \"function\" type required for callback');
                    return undefined;
                }
                if (method == 'POST') {
                    axios.post(url, data)
                        .then(function(response) {
                             if (response['data']['code'] == 0) {
                                 proc(response['data']);
                             }
                             else {
                                 exception(response['data']);
                             }
                        })
                        .catch(function(error) {
                             alert('Error occured!');
                        });
                }
                if (method == 'GET') {
                    axios.get(url, data).
                        then(function(response) {
                            if (response['data']['code'] == 0) {
                                proc(response['data']);
                            }
                            else {
                                exception(response['data']);
                            }
                        })
                        .catch(function(error) {
                            alert('Error occured!');
                        });
                }
                return this;
            } else {
                console.log('[err] \"string\" wanted as url but another type is received.')
            }
        }
    };
    testme.prototype.init.prototype = testme.prototype;
}(window, undefined));

const dev = device.default;
