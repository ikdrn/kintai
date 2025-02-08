<!-- kintai_front/src/App.vue -->
<template>
  <div>
    <Header :title="pageTitle" />
    <router-view @update-title="updateTitle"></router-view>
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: { Header },
  data() {
    return {
      pageTitle: '勤怠管理システム'
    }
  },
  methods: {
    updateTitle(newTitle) {
      this.pageTitle = newTitle
    }
  }
}
</script>

<style>
/* 必要に応じてスタイルを追加 */
</style>
