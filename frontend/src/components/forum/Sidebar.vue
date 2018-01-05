<template>
  <div :class="'column col-md-'+portion">
    <sidebar-messages></sidebar-messages>
  </div>
</template>

<script>
  import Messages from './Messages'

  export default {
    name: 'sidebar',
    props: ['portion'],
    components: {
      'sidebar-messages': Messages
    }
  }
</script>
