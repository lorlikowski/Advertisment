import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/users/:id/',
    name: 'User',
    props: route => ({
      id: route.params.id
    }),
    component: () => import('../views/User.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/create',
    name: 'Create',
    component: () => import('../views/AdvertisementEditorView.vue')
  },
  {
    path: '/edit/:id/',
    name: 'Edit',
    props: route => ({
      id: route.params.id
    }),
    component: () => import('../views/AdvertisementEditorView.vue')
  },
  {
    path: '/category/',
    props: route => ({
      page: route.query.page,
      perPage: route.query.perPage
    }),
    name: 'RootCategory',
    component: () => import('@/views/Category.vue')
  },
  {
    path: '/category/:category/',
    props: route => ({
      category: route.params.category,
      page: route.query.page,
      perPage: route.query.perPage
    }),
    name: 'Category',
    component: () => import('@/views/Category.vue')
  },
  {
    path: '/advertisement/:advertisement_id/',
    props: route => ({
      advertisement_id: route.params.advertisement_id,
      backlink: route.query.backlink
    }),
    name: 'AdvertisementView',
    component: () => import('@/views/AdvertisementView.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
