<template>
  <div :class="'col-md-'+portion">
    <div class="thumbnail">
      <img alt="300x200" :src="pic"/>
      <div class="caption center">
        <h3>
          {{title}}
        </h3>
        <p>
          {{content}}
        </p>
        <p>
          <a rel="nofollow" class="btn btn-primary" :href="url">浏览</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'news',
    props: ['portion', 'pic', 'title', 'content', 'url']
  }
</script>
