<template>
  <div :class="'column col-md-'+portion">
    <ul class="nav nav-pills">
      <li :class="{ 'active': selected === 0 }">
        <a rel="nofollow" href="#"> <span id="point-number" class="badge pull-right">{{ pn }}</span> 讨论热点</a>
      </li>
      <li :class="{ 'active': selected === 1 }">
        <a rel="nofollow" href="#"> <span id="tutorial-number" class="badge pull-right">{{ tn }}</span> 比赛教程</a>
      </li>
    </ul>
    <div id="posts">
      <post v-for="item in posts"
            :key="item.id"
            :post_id="item.id"
            :title="item.title"
            :contest="item.content"
            :time="item.time"
            :author="item.author"></post>
    </div>
    <div class="center">
      <ul id="pagination-list" class="pagination">
        <pagination v-for="item in pagination"
                    :key="item.tag"
                    :tag="item.tag"
                    @pagination-click="get_page"></pagination>
      </ul>
    </div>
    <form role="form">
      <div class="form-group">
        <label for="post-form-title">帖子标题</label><input type="email" class="form-control"
                                                        id="post-form-title"/>
      </div>
      <div class="form-group">
        <label for="post-form-content">帖子内容</label><textarea class="form-control" id="post-form-content"/>
      </div>
      <div class="form-group right">
        <button type="submit" class="btn btn-default">Submit</button>
      </div>
    </form>
  </div>
</template>

<script>
  import Vue from 'vue';
  import Post from './Post';

  let PaginationC = Vue.extend({
    name: 'pagination',
    props: ['tag'],
    template: `<li><button @click="$emit('pagination-click', tag)">{{tag}}</button></li>`,
  });

  export default {
    name: 'list-main',
    data() {
      return {
        get_url: "/api/c/forum/list",
        current_page: 1,
        max_pages: 1,
        user_id: this.$route.params.id,
        loaded: false,
        pagination: [],
        posts: []
      }
    },
    props: ['selected', 'portion', 'tn', 'pn'],
    components: {
      'post': Post,
      'pagination': PaginationC
    },
    mounted() {
      this.get_page('1');
    },
    methods: {
      get_page(page) {
        if (page === 'prev') {
          if(this.current_page === 1) {
            return;
          }
          else {
            page = this.current_page - 1;
          }
        }
        else if(page === 'next') {
          if(this.current_page === this.max_pages) {
            return;
          }
          else {
            page = this.current_page + 1;
          }
        }
        else {
          page = parseInt(page);
        }
        let url = this.get_url;
        let m = 'GET';
        let data = {
          "user_id": this.user_id,
          "page": page
        };
        let success = function (response) {
          if (!this.loaded) {
            this.max_pages = response.data['maxPages'];
            this.pagination.push({
              tag: "prev"
            });
            for (let i = 0; i < this.max_pages; ++i) {
              this.pagination.push({
                tag: '' + (i + 1)
              })
            }
            this.pagination.push({
              tag: "next"
            });
            this.loaded = true;
          }
          this.posts = [];
          data = this.response.data
          for (let i = 0; i < response.data['posts'].length; ++i) {
            this.posts.push({
              'id': data.id,
              'title': data.title,
              'content': data.content,
              'time': data.createTime,
              'author': data.authorName
            })
          }
          this.current_page = page;
        };
        let failed = function (response) {
          alert('[' + response.code.toString() + ']' + response.msg);
        };
        $t(url, m, data, success, failed);
      }
    }
  }
  /*
  提供参数：id：用户id page: 请求的页面号
  /api/p/forum/list  api definitions:
  {
    maxPages: after having paginated the posts, the max page num,
    posts: [the sorted post array:{id, title, content, createTime, authorName}]
  }
  */
</script>
