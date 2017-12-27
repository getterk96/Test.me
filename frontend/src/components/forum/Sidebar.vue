<template>
  <div :class="'column col-md-'+portion">
    <sidebar-follows></sidebar-follows>
    <sidebar-messages></sidebar-messages>
  </div>
</template>

<script>
  import Follows from './Follows'
  import Messages from './Messages'
  export default {
    name: 'sidebar',
    props: ['portion'],
    components: {
      'sidebar-follows': Follows,
      'sidebar-messages': Messages
    }
  }
</script>
