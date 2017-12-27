<template>
  <div id="detail" class="col-md-12 column">
    <detail-nav></detail-nav>
    <div class="row clearfix main-box">
      <detail-main portion="10"></detail-main>
      <detail-sidebar portion="2"></detail-sidebar>
    </div>
    <detail-footer></detail-footer>
  </div>
</template>

<script>
  import DetailNav from './Nav'
  import DetailSidebar from './Sidebar'
  import DetailFooter from './Footer'
  import DetailMain from './detail/Main'

  export default {
    name: 'detail',
    components: {
      'detail-nav': DetailNav,
      'detail-sidebar': DetailSidebar,
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
