<!-- kintai_front/src/components/Header.vue -->
<template>
  <header class="header">
    <h1>{{ title }}</h1>
    <div v-if="employee" class="user-info">
      <small>{{ employee.EMPLNM }} ({{ employee.EMPLID }})</small>
      <button @click="logout">ログアウト</button>
    </div>
  </header>
</template>

<script>
import { store } from '../store'
import { useRouter } from 'vue-router'

export default {
  name: 'Header',
  props: ['title'],
  computed: {
    employee() {
      return store.employee
    }
  },
  setup() {
    const router = useRouter()
    const logout = async () => {
      try {
        await fetch('http://localhost:8000/api/logout/', {
          method: 'POST',
          credentials: 'include'
        })
      } catch (error) {
        console.error(error)
      }
      store.employee = null
      router.push('/')
    }
    return { logout }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #f0f0f0;
}
.user-info {
  display: flex;
  align-items: center;
}
.user-info button {
  margin-left: 10px;
}
</style>
