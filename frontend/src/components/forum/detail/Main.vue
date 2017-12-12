<template>
  <div :class="'column col-md-'+portion">
    <ul class="nav nav-pills">
      <li :class="{ active: selected === 0 }">
        <a rel="nofollow" href="#"> <span id="announcement-number" class="badge pull-right">{{ an }}</span> 比赛公告</a>
      </li>
      <li :class="{ active: selected === 1 }">
        <a rel="nofollow" href="#"> <span id="tutorial-number" class="badge pull-right">{{ tn }}</span> 教程</a>
      </li>
      <li :class="{ active: selected === 2 }">
        <a rel="nofollow" href="#"> <span id="point-number" class="badge pull-right">{{ pn }}</span> 讨论热点</a>
      </li>
    </ul>
    <div id="abstracts">
      <main-abstract
        title="这是一个帖子"
        content="这里是帖子的内容"
        author="getterk"
        time="2017.12.09"></main-abstract>
            <main-abstract
        title="这是一个帖子"
        content="这里是帖子的内容"
        author="getterk"
        time="2017.12.09"></main-abstract>
            <main-abstract
        title="这是一个帖子"
        content="这里是帖子的内容"
        author="getterk"
        time="2017.12.09"></main-abstract>
            <main-abstract
        title="这是一个帖子"
        content="这里是帖子的内容"
        author="getterk"
        time="2017.12.09"></main-abstract>
            <main-abstract
        title="这是一个帖子"
        content="这里是帖子的内容"
        author="getterk"
        time="2017.12.09"></main-abstract>
            <main-abstract
        title="这是一个帖子"
        content="这里是帖子的内容"
        author="getterk"
        time="2017.12.09"></main-abstract>
            <main-abstract
        title="这是一个帖子"
        content="这里是帖子的内容"
        author="getterk"
        time="2017.12.09"></main-abstract>
    </div>
  </div>
</template>

<script>
  import Abstract from './Abstract'
  export default {
    name: 'main',
    props: ['selected', 'portion', 'an', 'tn', 'pn'],
    components: {
      'main-abstract': Abstract
    },
    methods: {
      getAbstracts: function () {
      }
    }
  }
</script>
