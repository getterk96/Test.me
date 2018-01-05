<template>
  <div :class="'column col-md-'+portion">
    <div class="jumbotron">
				<h1 class="shift_right">
					{{this.title}}
				</h1>
				<p class="shift_right">
          {{this.content}}
				<p class="shift_right">
          <a class="btn btn-primary btn-large" :href='"/forum?uid="+user_id+"&cid="+contest_id'>返回讨论区</a>
				</p>
    </div>

    <div id="replys">
      <reply v-for="item in replies"
            :key="item.id"
            :title="item.title"
            :content="item.content"
            :time="item.time"
            :author="item.author"></reply>
    </div>
    <div class="center">
      <ul id="pagination-list" class="pagination">
        <pagination v-for="item in pagination"
                    :key="item.tag"
                    :tag="item.tag"
                    @pagination-click="get_page"></pagination>
      </ul>
    </div>
    <form role="form" @submit.prevent="create_reply">
      <div class="form-group">
        <label for="reply-form-title">回复标题</label><input v-model="new_reply.title" type="text" class="form-control"
                                                         id="reply-form-title"/>
      </div>
      <div class="form-group">
        <label for="reply-form-content">回复内容</label><textarea v-model="new_reply.content" class="form-control"
                                                              id="reply-form-content"/>
      </div>
      <div class="form-group right">
        <button type="submit" class="btn btn-default">Submit</button>
      </div>
    </form>
  </div>
</template>

<script>
  import Vue from 'vue';
  import Reply from './Reply';

  let PaginationC = Vue.extend({
    name: 'pagination',
    props: ['tag'],
    template: `<li><button @click="$emit('pagination-click', tag)">{{tag}}</button></li>`,
  });

  export default {
    name: 'detail-main',
    data() {
      return {
        get_url: '/api/c/forum/detail',
        post_url: '/api/c/forum/reply/create',
        default_page_replies: 5,
        title: '',
        content: '',
        author: '',
        time: '',
        current_page: 1,
        max_pages: 1,
        loaded: false,
        post_id: this.$route.query.pid,
        user_id: this.$route.query.uid,
        contest_id: this.$route.query.cid,
        pagination: [],
        replies: [],
        new_reply: {
          title: '',
          content: '',
          user_id: this.$route.query.uid,
          post_id: this.$route.query.pid
        }
      }
    },
    props: ['selected', 'portion', 'tn', 'pn'],
    components: {
      'reply': Reply,
      'pagination': PaginationC
    },
    mounted() {
      this.get_page('1');
    },
    methods: {
      page_get_success: function (response) {
        this.max_pages = response.data['maxLen'];
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
        this.replies = [];
        let data = response.data['replies'];
        for (let i = 0; i < data.length; ++i) {
          this.replies.push({
            'id': data[i]['id'],
            'title': data[i]['title'],
            'content': data[i]['content'],
            'time': data[i]['createTime'],
            'author': data[i]['authorName'],
          })
        }
        this.title = response.data['title'];
        this.content = response.data['content'];
        this.time = response.data['createTime'];
        this.author = response.data['author']
      },
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
        this.current_page = page;
        let url = this.get_url;
        let m = 'GET';
        let data = {
          'user_id': this.user_id,
          'post_id': this.post_id,
          'page': page
        };
        let failed = function (response) {
          alert('[' + response.code.toString() + ']' + response.msg);
        };
        $t(url, m, data, this.page_get_success, failed);
      },
      create_success: function (response) {
        if (this.replies.length === this.default_page_replies)
          this.get_page(this.max_pages + 1);
        else
          this.get_page(this.max_pages)
      },
      create_reply: function () {
        let url = this.post_url;
        let m = 'POST';
        let data = {
          title: this.new_reply.title,
          content: this.new_reply.content,
          user_id: this.user_id,
          post_id: this.post_id
        };
        let failed = function (response) {
          alert('[' + response.code.toString() + ']' + response.msg);
        };
        $t(url, m, data, this.create_success, failed);
      }
    }
  }
  /*
  /api/p/forum/detail api definitions:
  {
    maxPages: after having paginated the replies, the max page num,
    replies: [the sorted reply array:{id, title, content, createTime, authorName}]
  }
  */
</script>

<style>
  .shift_right{
    margin-left: 50px;
  }
</style>
