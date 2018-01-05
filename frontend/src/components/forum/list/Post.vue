<template>
  <div class="panel panel-default">
    <div class="panel-heading">
      <h3 class="panel-title">
        <router-link :to="{ path: '/forum/detail', query: { pid: post_id, uid: user_id, cid: contest_id }}">{{ title }}</router-link>
      </h3>
    </div>
    <div class="panel-body">
      {{ content }}
    </div>
    <div class="panel-footer right">
      {{ author }} {{ time }}
    </div>
  </div>
</template>

<script>
  export default {
    name: 'abstract',
    props: ['user_id', 'post_id', 'contest_id', 'title', 'content', 'author', 'time']
  }
</script>
