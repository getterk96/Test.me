import Vue from 'vue'
import Router from 'vue-router'
import List from '@/components/forum/List'
import Detail from '@/components/forum/Detail'

Vue.use(Router)

export default new Router({
  linkActiveClass: 'active',
  hashbang: false, // 将路径格式化为#!开头
  history: false, // 启用HTML5 history模式，可以使用pushState和replaceState来管理记录
  mode: 'history',
  /**
   * @desc 路由配置
   */
  routes: [
    {
      path: '/forum/detail',
      name: 'Detail',
      component: Detail
    },
    {
      path: '/forum/list',
      name: 'List',
      component: List
    },
    {
      path: '/forum',
      redirect: '/forum/list'
    }
  ]
})
