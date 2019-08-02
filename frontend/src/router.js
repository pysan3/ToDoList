import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/about', component: 'About' },
  { path: '*', component: 'HelloWorld' },
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    name: `${route.component}`.toLowerCase(),
    component: () => import(`@/components/${route.component}.vue`)
  }
})

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
