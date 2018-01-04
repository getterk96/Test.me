<template>
  <div :class="'column col-md-'+portion">
    <div class="page-header">
      <h1>
        {{owner}}
        <small>个人主页</small>
      </h1>
    </div>
    <div id="posts"></div>
    <div class="center">
      <ul id="pagination-list" class="pagination">
        <pagination v-for="item in pagination"
                    :key="item.tag"
                    :tag="item.tag"
                    @pagination-click="change_page"></pagination>
      </ul>
    </div>
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
    name: 'peronal-main',
    data() {
      return {
        get_url: "/api/c/forum/personal",
        current_page: 1,
        max_pages: 1,
        owner: None,
        pagination: []
      }
    },
    props: ['portion'],
    components: {
      'post': Post,
      'pagination': PaginationC
    },
    mounted() {
      this.on();
      this.change_page({'tag': '1'});
    },
    methods: {
      on: (function () {
        $t(this.get_url, 'GET', {},
          function (response) {
            this.max_pages = response.data['maxPages'];
          },
          function () {
            this.max_pages = 1;
            alert('[' + response.code.toString() + ']' + response.msg);
          });
        this.current_page = 1;
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
      }),
      change_page(tag) {
        let url = '';
        if (tag === 'prev') {
          url = this.get_url + '?page=' + (this.current_page === 1 ? 1 : --this.current_page);
        }
        else if (tag === 'next') {
          url = this.get_url + '?page=' + (this.current_page === this.max_pages ? this.max_pages : ++this.current_page)
        }
        else {
          url = this.get_url + '?page=' + tag;
        }
        let m = 'GET';
        let data = {};
        let success = function () {

        };
        let failed = function (response) {
          alert('[' + response.code.toString() + ']' + response.msg);
        };
        $t(url, m, data, success, failed);
      }
    }
  }
  /*
  /api/c/forum/personal api definitions:
  {
    maxPages: after having paginated the replies, the max page num,
  }
  /api/p/forum/personal?page=xxx api definitions:
  {
    len: the reply array length no more than 10,
    replies: [the sorted reply array:{id, title, content, createTime, authorName}]
  }
  */
</script>
