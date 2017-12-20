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
    <div id="abstracts"></div>
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
    name: 'list-main',
    data() {
      return {
        get_url: "/api/p/forum/list",
        current_page: 1,
        max_pages: 1,
        pagination: []
      }
    },
    props: ['selected', 'portion', 'tn', 'pn'],
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
      change_page (tag) {
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
  /api/p/forum/list api definitions:
  {
    maxPages: after having paginated the posts, the max page num,
  }
  /api/p/forum/list?page=xxx api definitions:
  {
    len: the post array length no more than 10,
    posts: [the sorted post array:{id, title, content, createTime, authorName}]
  }
  */
</script>
