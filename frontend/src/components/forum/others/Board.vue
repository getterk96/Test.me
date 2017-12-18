<template>
  <div class="row">
    <info-news pic="" portion="4" title="新闻一" content="这里是内容"></info-news>
    <info-news pic="" portion="4" title="新闻一" content="这里是内容"></info-news>
    <info-news pic="" portion="4" title="新闻一" content="这里是内容"></info-news>
  </div>
</template>

<script>
  import News from './News'
  export default {
    name: 'board',
    components: {
      'info-news': News
    },
    methods: {
      getNews: function () {}
    }
  }
</script>
