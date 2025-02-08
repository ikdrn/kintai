<!-- kintai_front/src/views/Attendance.vue -->
<template>
  <div class="attendance">
    <div class="calendar-container">
      <div class="calendar-header">
        <button @click="prevMonth">&lt;</button>
        <span>{{ currentYear }}年{{ currentMonth }}月</span>
        <button @click="nextMonth">&gt;</button>
      </div>
      <table class="calendar-table">
        <thead>
          <tr>
            <th v-for="day in weekDays" :key="day">{{ day }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(week, wIndex) in calendar" :key="wIndex">
            <td v-for="(day, dIndex) in week" :key="dIndex" :class="{ 'today': isToday(day.date), 'selected': isSelected(day.date) }" @click="selectDate(day.date)">
              <span v-if="day.inMonth">{{ day.date.getDate() }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="detail-panel" v-if="selectedDate">
      <h3>{{ selectedDateStr }}</h3>
      <div>
        <label>就業時間:</label>
        <input type="time" v-model="detail.startTime" />
      </div>
      <div>
        <label>終了時間:</label>
        <input type="time" v-model="detail.endTime" />
      </div>
      <div>
        <button @click="saveAttendance">保存</button>
      </div>
      <div v-if="message" class="message">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { store } from '../store'

export default {
  name: 'Attendance',
  data() {
    return {
      currentDate: new Date(),
      selectedDate: null,
      detail: {
        startTime: '09:00',
        endTime: '18:00'
      },
      attendanceRecords: {}, // key: 'YYYY-MM-DD'、value: { startTime, endTime }
      message: ''
    }
  },
  computed: {
    currentYear() {
      return this.currentDate.getFullYear()
    },
    currentMonth() {
      return this.currentDate.getMonth() + 1
    },
    weekDays() {
      return ['日', '月', '火', '水', '木', '金', '土']
    },
    // カレンダー用の2次元配列を生成
    calendar() {
      const year = this.currentDate.getFullYear()
      const month = this.currentDate.getMonth()
      const firstDay = new Date(year, month, 1)
      const lastDay = new Date(year, month + 1, 0)
      const startDayOfWeek = firstDay.getDay()  // 日曜日=0
      const totalDays = lastDay.getDate()
      let calendar = []
      let week = []
      // 先頭の空セル
      for (let i = 0; i < startDayOfWeek; i++) {
        week.push({ date: null, inMonth: false })
      }
      for (let day = 1; day <= totalDays; day++) {
        const date = new Date(year, month, day)
        week.push({ date: date, inMonth: true })
        if (week.length === 7) {
          calendar.push(week)
          week = []
        }
      }
      // 週の末尾を埋める
      if (week.length) {
        while (week.length < 7) {
          week.push({ date: null, inMonth: false })
        }
        calendar.push(week)
      }
      return calendar
    },
    selectedDateStr() {
      if (!this.selectedDate) return ''
      return this.selectedDate.toISOString().split('T')[0]
    }
  },
  methods: {
    isToday(date) {
      if (!date) return false
      const today = new Date()
      return date.toDateString() === today.toDateString()
    },
    isSelected(date) {
      if (!date || !this.selectedDate) return false
      return date.toDateString() === this.selectedDate.toDateString()
    },
    prevMonth() {
      const year = this.currentDate.getFullYear()
      const month = this.currentDate.getMonth()
      this.currentDate = new Date(year, month - 1, 1)
      this.fetchAttendance()
    },
    nextMonth() {
      const year = this.currentDate.getFullYear()
      const month = this.currentDate.getMonth()
      this.currentDate = new Date(year, month + 1, 1)
      this.fetchAttendance()
    },
    selectDate(date) {
      if (!date) return
      this.selectedDate = date
      const dateKey = date.toISOString().split('T')[0]
      // すでに登録済みの勤怠データがあれば反映、なければ初期値
      if (this.attendanceRecords[dateKey]) {
        this.detail = { ...this.attendanceRecords[dateKey] }
      } else {
        this.detail = { startTime: '09:00', endTime: '18:00' }
      }
    },
    async fetchAttendance() {
      // ログイン済みでなければログイン画面へ
      if (!store.employee) {
        this.$router.push('/')
        return
      }
      const year = this.currentDate.getFullYear()
      const month = this.currentDate.getMonth() + 1
      try {
        const response = await fetch(`http://localhost:8000/api/attendance/?year=${year}&month=${month}`, {
          method: 'GET',
          credentials: 'include'
        })
        const resData = await response.json()
        if (resData.success) {
          this.attendanceRecords = {}
          resData.data.forEach(record => {
            this.attendanceRecords[record.date] = {
              startTime: record.startTime,
              endTime: record.endTime
            }
          })
        } else {
          this.message = resData.message
        }
      } catch (error) {
        console.error(error)
        this.message = '勤怠データ取得エラー'
      }
    },
    async saveAttendance() {
      if (!this.selectedDate) return
      const dateKey = this.selectedDate.toISOString().split('T')[0]
      try {
        const response = await fetch('http://localhost:8000/api/attendance/update/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({
            date: dateKey,
            startTime: this.detail.startTime,
            endTime: this.detail.endTime
          })
        })
        const resData = await response.json()
        if (resData.success) {
          this.attendanceRecords[dateKey] = { ...this.detail }
          this.message = '保存しました'
        } else {
          this.message = resData.message || '保存に失敗しました'
        }
      } catch (error) {
        console.error(error)
        this.message = '保存エラー'
      }
    }
  },
  mounted() {
    // ログインチェック
    if (!store.employee) {
      this.$router.push('/')
      return
    }
    this.fetchAttendance()
  }
}
</script>

<style scoped>
.attendance {
  display: flex;
  gap: 20px;
  padding: 20px;
}
.calendar-container {
  flex: 1;
}
.detail-panel {
  flex: 0 0 300px;
  border: 1px solid #ccc;
  padding: 10px;
}
.calendar-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}
.calendar-header button {
  margin: 0 10px;
}
.calendar-table {
  width: 100%;
  border-collapse: collapse;
}
.calendar-table th, .calendar-table td {
  width: 14.28%;
  height: 50px;
  text-align: center;
  border: 1px solid #ddd;
  cursor: pointer;
}
.calendar-table td.today {
  background-color: #fdd;
}
.calendar-table td.selected {
  background-color: #dfd;
}
</style>
