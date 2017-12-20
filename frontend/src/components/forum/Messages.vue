<template>
  <div>
    <h3>我的动态</h3>
    <ol>
      <message
        v-for="item in messages"
        :key="item.id"
        :id="item.id"
        :title="item.title"
        :url="item.url"></message>
    </ol>
  </div>
</template>

<script>
  import Vue from 'vue'

  let messageC = Vue.extend({
    name: 'messageC',
    template: '<li><a :href="url">{{title}}</a></li>',
    props: ['title', 'url']
  });

  export default {
    components: {
      'message': messageC,
    },
    data() {
      return {
        messages: [],
        other_url: ''
      }
    },
    mounted() {
      this.on()
    },
    methods: {
      on: (function () {
        let url = '/api/p/forum/messages';
        let m = 'GET';
        let data = {};
        let success = function (response) {
          let data = response.data;
          for (let i = 0; i < data.len; i++) {
            this.messages.push({
              id: "message-" + i,
              url: data.messages[i].url,
              title: data.messages[i].title
            });
          }
          other_url = data.url;
          this.messages.push({
            id: 'other-messages',
            url: other_url,
            title: '其他'
          });
        };
        let failed = function (response) {
          alert('[' + response.code.toString() + ']' + response.msg);
        };
        $t(url, m, data, success, failed);
      })
    }

  };
  /*
  api definitions:
  {
    len: the message array length no more than 10,
    messages: [the message array:{title, url: the message detail page url in personal center}],
    url: personal center message list page url,
  }
  */
</script>

