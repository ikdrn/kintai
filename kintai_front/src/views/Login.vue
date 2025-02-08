<!-- kintai_front/src/views/Login.vue -->
<template>
  <div class="login">
    <h2>ログイン</h2>
    <form @submit.prevent="login">
      <div>
        <label for="employeeId">社員番号（5桁）:</label>
        <input id="employeeId" v-model="employeeId" autocomplete="off" maxlength="5" required />
      </div>
      <div>
        <button type="submit">ログイン</button>
      </div>
      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import { store } from '../store'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  data() {
    return {
      employeeId: '',
      error: ''
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  methods: {
    async login() {
      this.error = ''
      try {
        const response = await fetch('http://localhost:8000/api/login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include', // セッション維持のために必要
          body: JSON.stringify({ employeeId: this.employeeId })
        })

        // もしレスポンスが正常でなければエラーテキストを取得してログ出力
        if (!response.ok) {
          const errorText = await response.text();
          console.error("Error response:", errorText);
          this.error = `サーバーエラー: ${response.status}`;
          return;
        }

        const resData = await response.json();
        if (resData.success) {
          // グローバルストアにログイン情報を保存
          store.employee = resData.employee
          // 勤怠入力画面へ遷移
          this.$router.push('/attendance')
        } else {
          this.error = resData.message || 'ログイン失敗'
        }
      } catch (error) {
        this.error = 'エラーが発生しました'
        console.error(error)
      }
    }
  },
  mounted() {
    // ログイン済みなら勤怠画面へリダイレクト
    if (store.employee) {
      this.$router.push('/attendance')
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
}
</style>
