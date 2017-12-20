<template>
  <div>
    <h3>
      我的关注
    </h3>
    <ol>
      <li>
        <a id="follow-1" href="#">周一念</a>
      </li>
      <li>
        <a id="follow-2" href="#">韦宇华</a>
      </li>
      <li>
        <a id="follow-3" href="#">冯玉彤</a>
      </li>
      <li>
        <a id="follow-4" href="#">周杰伦</a>
      </li>
      <li>
        <a id="follow-5" href="#">林徽音</a>
      </li>
      <li>
        <a id="follow-others" href="#">其他</a>
      </li>
    </ol>
  </div>
</template>

<script>
  import Vue from 'vue'

  let followC = Vue.extend({
    name: 'followC',
    template: '<li><a :href="url">{{title}}</a></li>',
    props: ['title', 'url']
  });

  export default {
    components: {
      'follow': followC,
    },
    data() {
      return {
        follows: [],
        other_url: ''
      }
    },
    mounted() {
      this.on()
    },
    methods: {
      on: (function () {
        let url = '/api/p/forum/follows';
        let m = 'GET';
        let data = {};
        let success = function (response) {
          let data = response.data;
          for (let i = 0; i < data.len; i++) {
            this.follows.push({
              id: "follow-" + i,
              url: data.follows[i].url,
              title: data.follows[i].title
            });
          }
          other_url = data.url;
          this.follows.push({
            id: 'other-follows',
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
    len: the follow array length no more than 10,
    follows: [the follow array:{title, url: the follow detail page url in personal center}],
    url: personal center follow list page url,
  }
  */
</script>
