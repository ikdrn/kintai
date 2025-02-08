// kintai_front/src/store.js
import { reactive } from 'vue'

export const store = reactive({
  employee: null  // { EMPLID: 'xxxxx', EMPLNM: '名前' } の形式
})
