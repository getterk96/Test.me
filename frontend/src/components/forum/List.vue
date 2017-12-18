<template>
  <div id="list" class="col-md-12 column">
    <list-nav></list-nav>
    <div class="row clearfix main-box">
      <list-main portion="10" tn="99+" pn="99+" :selected="default_column"></list-main>
      <list-sidebar portion="2"></list-sidebar>
    </div>
    <list-footer></list-footer>
  </div>
</template>

<script>
  import Nav from './Nav'
  import ListMain from './list/Main'
  import Sidebar from './Sidebar'
  import Footer from './Footer'

  export default {
    name: 'list',
    data: function () {
      return {
        default_column: 0,
      }
    },
    components: {
      'list-nav': Nav,
      'list-main': ListMain,
      'list-sidebar': Sidebar,
      'list-footer': Footer
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
