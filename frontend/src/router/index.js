import Vue from 'vue'
import Router from 'vue-router'
import List from '@/components/forum/List'

Vue.use(Router)

export default new Router({
  linkActiveClass: 'active',
  hashbang: true, // 将路径格式化为#!开头
  history: true, // 启用HTML5 history模式，可以使用pushState和replaceState来管理记录
  /**
   * @desc 路由配置
   */
  routes: [
    {
      path: '/',
      name: 'List',
      component: List
    },
    {
      path: '/forum/list',
      name: 'List',
      component: List
    },
  ]
})
