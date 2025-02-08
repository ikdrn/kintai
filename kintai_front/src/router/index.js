// kintai_front/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Attendance from '../views/Attendance.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/attendance',
    name: 'Attendance',
    component: Attendance
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
