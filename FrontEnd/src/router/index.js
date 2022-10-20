import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Likes from '../views/Likes.vue'
import config from '../views/config.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/userlist',
      name: 'userlist',
      //chargé uniquement quand visitée
      component: Likes,
    },
    {
      path: '/config',
      name: 'config',
      //chargé uniquement quand visitée
      component: config,
    },
    {
      path:'/:pathMatch(.*)*',
      name: 'all',
      component: HomeView
    }
  ]
})

export default router
