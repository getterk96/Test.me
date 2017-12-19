<template>
  <div :class="'column col-md-'+portion">
    <h3>
      {{title}}
    </h3>
    <p>
      {{content}}
    </p>
    <div id="replys"></div>
    <pagination></pagination>
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
  import Reply from './Reply'
  import Pagination from '../Pagination'
  export default {
    name: 'detail-main',
    props: ['portion', 'title', 'content'],
    components: {
      'reply': Reply,
      'pagination': Pagination
    },
    methods: {
      getReplys: function () {
      }
    }
  }
</script>
