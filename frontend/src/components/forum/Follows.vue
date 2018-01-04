<template>
  <div>
    <h3>
      我的关注
    </h3>
    <ol>
      <follow v-for="item in follows"
              :key="item.id"
              :id="item.id"
              :title="item.title"
              :url="item.url"></follow>
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
      'follow': followC
    },
    data() {
      return {
        follows: [],
        other_url: '',
        user_id: this.$route.params.id
      }
    },
    mounted() {
      let url = '/api/c/forum/follows';
        let m = 'GET';
        let data = {
          'user_id': this.user_id
        };
        let success = function (response) {
          let data = response.data;
          this.follows = [];
          for (let i = 0; i < data.length; i++) {
            this.follows.push({
              id: "follow-" + i,
              url: data.follows[i].url,
              title: data.follows[i].title
            });
          }
          other_url = data.otherUrl;
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
    }
  };
  /*
  api definitions:
  {
    len: the follow array length no more than 10,
    follows: [the follow array:{title, url: the follow detail page url in personal center}],
    otherUrl: personal center follow list page url,
  }
  */
</script>
