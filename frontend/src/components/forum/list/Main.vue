<template>
  <div :class="'column col-md-'+portion">
    <ul class="nav nav-pills">
      <li :class="{ 'active': selected === 0 }">
        <a rel="nofollow" href="#"> <span id="point-number" class="badge pull-right">{{ pn }}</span> 讨论热点</a>
      </li>
      <li :class="{ 'active': selected === 1 }">
        <a rel="nofollow" href="#"> <span id="tutorial-number" class="badge pull-right">{{ tn }}</span> 比赛教程</a>
      </li>
    </ul>
    <div id="abstracts"></div>
    <pagination></pagination>
  </div>
</template>

<script>
  import Post from './Post'
  import Pagination from '../Pagination'
  export default {
    name: 'main',
    props: ['selected', 'portion', 'tn', 'pn'],
    components: {
      'post': Post,
      'pagination': Pagination
    },
    methods: {
      getPosts: function () {
      }
    }
  }
</script>
