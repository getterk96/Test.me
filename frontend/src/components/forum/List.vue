<template>
  <div id="list" class="col-md-12 column">
    <list-nav></list-nav>
    <div class="row clearfix">
      <list-main portion="10" tn="99+" pn="99+" selected="0"></list-main>
      <list-sidebar portion="2"></list-sidebar>
    </div>
    <list-footer></list-footer>
  </div>
</template>

<script>
  import ListNav from './list/Nav'
  import ListMain from './list/Main'
  import ListSidebar from './list/Sidebar'
  import ListFooter from './list/Footer'

  export default {
    name: 'list',
    components: {
      'list-nav': ListNav,
      'list-main': ListMain,
      'list-sidebar': ListSidebar,
      'list-footer': ListFooter
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
