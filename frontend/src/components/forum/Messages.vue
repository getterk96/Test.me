<template>
  <div>
    <h3>
      我的动态
    </h3>
    <ol id='message_list'>
    </ol>
  </div>
</template>

<script>
  import Vue from 'vue'

  export default {
    name: 'messages',
    components: {
      'message': messageC,
    }
  };

  let messages = [];
  let other_url = "";

  let messageC = Vue.extend({
    name: 'message',
    template: '<li><a>{{content}}</a></li>',
    props: ['content']
  });

  (function () {
    let url = '/api/p/forum/message';
    let m = 'GET';
    let data = {};
    let success = function (response) {
      let data = response.data;
      for (let i = 0; i < data.len; i++) {
        messages.append({
          id: "message-" + i,
          url: data.messages[i].url,
          title: data.messages[i].title
        });
        document.getElementById("#message_list").appendChild(
          document.createElement("message")
            .setAttribute("id", messages[i].id)
            .setAttribute("href", messages[i].url)
            .setAttribute("content", messages[i].title)
        )
      }
      other_url = data.url;
      document.getElementById("#message_list").appendChild(
        document.createElement("message")
          .setAttribute("id", "other-url")
          .setAttribute("href", other_url)
          .setAttribute("content", "其他")
      );
    };
    let failed = function (response) {
      alert('[' + response.code.toString() + ']' + response.msg);
    };
    $t(url, 'GET', {}, success, failed);
  })();
  /*
  api definitions:
  {
    len: the message array length no more than 10,
    messages: [the message array:{title, url: the message detail page url in personal center}],
    url: personal center message list page url,
  }
   */
</script>

