import Vue from 'vue'
import Router from 'vue-router'
import List from '@/components/forum/List'
import Detail from '@/components/forum/Detail'
import Personal from '@/components/forum/Personal'

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
      path: '/forum/detail/:fid',
      name: 'Detail',
      component: Detail
    },
    {
      path: '/forum/personal/:id',
      name: 'Personal',
      component: Personal
    },
    {
      path: '/forum/list/:id',
      name: 'List',
      component: List
    },
    {
      path: '/',
      redirect: '/forum/list'
    }
  ]
})
