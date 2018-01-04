<template>
  <div :class="'column col-md-'+portion">
    <h3>
      {{this.title}}
    </h3>
    <p>
      {{this.content}}
    </p>
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
    <form role="form">
      <div class="form-group">
        <label for="reply-form-title">回复标题</label><input type="email" class="form-control"
                                                         id="reply-form-title"/>
      </div>
      <div class="form-group">
        <label for="reply-form-content">回复内容</label><textarea class="form-control"
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
        title: '',
        content: '',
        current_page: 1,
        max_pages: 1,
        loaded: false,
        post_id: this.$route.params.pid,
        pagination: [],
        replies: []
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
          "post_id": this.post_id,
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
          this.replies = [];
          data = this.response.data;
          for (let i = 0; i < response.data['replies'].length; ++i) {
            this.replies.push({
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
  /api/p/forum/detail api definitions:
  {
    maxPages: after having paginated the replies, the max page num,
    replies: [the sorted reply array:{id, title, content, createTime, authorName}]
  }
  */
</script>
