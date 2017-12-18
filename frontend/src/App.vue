<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>

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
    let _$t = window.$t;
    let _testme = window.testme;
    let testme = $t = window.$t = window.testme = function(url, method, data, proc, exception, proc_param, exception_param) {
        return new testme.prototype.init(url, method, data, proc, exception, proc_param, exception_param);
    }
    testme.fn = testme.prototype = {
        init : function(url, method, data, proc, exception, proc_param, exception_param) {
            proc_param = proc_param || {};
            exception_param = exception_param || {};
            if (typeof url === 'string') {
                if ((method !== 'POST') && (method !=='GET')) {
                    console.log('[err] invlalid method');
                    return undefined;
                }
                try {
                    data_str = JSON.stringify(data);
                } catch (e) {
                    console.log('[err] invalid json syntax');
                    return undefined
                }
                if ((typeof proc !== 'function') || (typeof exception !== 'function')) {
                    console.log('[err] \"function\" type required for callback');
                    return undefined;
                }
                if (method === 'POST') {
                    axios.post(url, data)
                        .then(function(response) {
                             if (response['data']['code'] === 0) {
                                 proc(response['data'], proc_param);
                             }
                             else {
                                 exception(response['data'], exception_param);
                             }
                        })
                        /*.catch(function(error) {
                             alert('Error occured!');
                        })*/;
                }
                if (method === 'GET') {
                    axios.get(url, {params : data}).
                        then(function(response) {
                            if (response['data']['code'] === 0) {
                                proc(response['data'], proc_param);
                            }
                            else {
                                exception(response['data'], exception_param);
                            }
                        })
                        /*.catch(function(error) {
                            alert('Error occured!');
                        })*/;
                }
                return this;
            } else {
                console.log('[err] \"string\" wanted as url but another type is received.')
            }
        }
    };
    testme.prototype.init.prototype = testme.prototype;
}(window, undefined));

</script>

<style>
  .main-box{
    max-width: 1000px;
    margin: auto;
  }
</style>
