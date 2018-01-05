<template>
  <div :class="'column col-md-'+portion">
    <h1>{{contest}}-比赛讨论区</h1>
    <ul class="nav nav-pills">
      <li :class="{ 'active': selected === 0 }">
        <a rel="nofollow" :href='"/forum?uid="+user_id+"&cid="+contest_id'><span id="point-number" class="badge pull-right">{{ pn }}</span> 讨论热点</a>
      </li>
    </ul>
    <div id="posts">
      <post v-for="item in posts"
            :key="item.id"
            :post_id="item.id"
            :title="item.title"
            :content="item.content"
            :time="item.time"
            :author="item.author"
            :user_id="user_id"
            :contest_id="contest_id"></post>
    </div>
    <div class="center">
      <ul id="pagination-list" class="pagination">
        <pagination v-for="item in pagination"
                    :key="item.tag"
                    :tag="item.tag"
                    @pagination-click="get_page"></pagination>
      </ul>
    </div>
    <form role="form" @submit.prevent="create_post">
      <div class="form-group">
        <label for="post-form-title">帖子标题</label><input v-model="new_post.title" type="text" class="form-control"
                                                        id="post-form-title"/>
      </div>
      <div class="form-group">
        <label for="post-form-content">帖子内容</label><textarea v-model="new_post.content" class="form-control"
                                                             id="post-form-content"/>
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
        get_url: '/api/c/forum/list',
        post_url: '/api/c/forum/post/create',
        default_page_posts: 5,
        current_page: 1,
        max_pages: 1,
        contest: '',
        user_id: this.$route.query.uid,
        contest_id: this.$route.query.cid,
        pagination: [],
        posts: [],
        new_post: {
          title: '',
          content: '',
          user: this.$route.query.uid,
          contest: this.$route.query.cid
        }
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
      page_get_success: function (response) {
        this.max_pages = response.data['maxLen'];
        this.contest = response.data['contestName'];
        this.pagination = [];
        this.pagination.push({
          tag: 'prev'
        });
        for (let i = 0; i < this.max_pages; ++i) {
          this.pagination.push({
            tag: '' + (i + 1)
          })
        }
        this.pagination.push({
          tag: 'next'
        });
        this.posts = [];
        let data = response.data['posts'];
        for (let i = 0; i < data.length; ++i) {
          this.posts.push({
            'id': data[i]['id'],
            'title': data[i]['title'],
            'content': data[i]['content'],
            'time': data[i]['createTime'],
            'author': data[i]['authorName'],
          })
        }
      },
      get_page: function (page) {
        if (page === 'prev') {
          if (this.current_page === 1) {
            return;
          }
          else {
            page = this.current_page - 1;
          }
        }
        else if (page === 'next') {
          if (this.current_page === this.max_pages) {
            return;
          }
          else {
            page = this.current_page + 1;
          }
        }
        else {
          page = parseInt(page);
        }
        this.current_page = page;
        let url = this.get_url;
        let m = 'GET';
        let data = {
          contest_id: this.contest_id,
          page: page
        };
        let failed = function (response) {
          alert('[' + response.code.toString() + ']' + response.msg);
        };
        $t(url, m, data, this.page_get_success, failed);
      },
      create_success: function (response) {
        if (this.posts.length === this.default_page_posts)
          this.get_page(this.max_pages + 1);
        else
          this.get_page(this.max_pages)
      },
      create_post: function () {
        let url = this.post_url;
        let m = 'POST';
        let data = {
          title: this.new_post.title,
          content: this.new_post.content,
          user_id: this.user_id,
          contest_id: this.contest_id
        };
        let failed = function (response) {
          alert('[' + response.code.toString() + ']' + response.msg);
        };
        $t(url, m, data, this.create_success, failed);
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
