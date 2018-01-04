<template>
  <div id="personal" class="col-md-12 column">
    <personal-nav></personal-nav>
    <div class="row clearfix main-box">
      <personal-main portion="10" :user_id="this.$route.params.id" ></personal-main>
      <personal-sidebar portion="2"></personal-sidebar>
    </div>
    <personal-footer></personal-footer>
  </div>
</template>

<script>
  import personalNav from './Nav'
  import personalMain from './personal/Main'
  import personalSidebar from './Sidebar'
  import personalFooter from './Footer'

  export default {
    name: 'personal',
    data: function () {
      return {
        default_column: 0,
      }
    },
    components: {
      'personal-nav': personalNav,
      'personal-main': personalMain,
      'personal-sidebar': personalSidebar,
      'personal-footer': personalFooter
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
