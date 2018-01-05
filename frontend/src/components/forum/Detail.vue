<template>
  <div id="detail" class="col-md-12 column">
    <detail-nav></detail-nav>
    <div class="clearfix main-box">
      <detail-main portion="12"></detail-main>
    </div>
    <detail-footer></detail-footer>
  </div>
</template>

<script>
  import DetailNav from './Nav'
  import DetailFooter from './Footer'
  import DetailMain from './detail/Main'

  export default {
    name: 'detail',
    components: {
      'detail-nav': DetailNav,
      'detail-footer': DetailFooter,
      'detail-main': DetailMain
    }
  }
</script>

<style>
  .center {
    text-align: center;
  }
  .right {
    text-align: right;
  }
</style>
