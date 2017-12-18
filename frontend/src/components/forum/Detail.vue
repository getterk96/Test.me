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
  import Nav from './Nav'
  import Sidebar from './Sidebar'
  import Footer from './Footer'
  import Main from './detail/Main'

  export default {
    name: 'detail',
    components: {
      'detail-nav': Nav,
      'detail-sidebar': Sidebar,
      'detail-footer': Footer,
      'detail-main': Main
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
