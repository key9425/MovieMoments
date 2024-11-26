<template>
  <section class="timeline-section">
    <!-- 타임라인 입력 폼 -->
    <div class="timeline-form-card">
      <h3 class="form-title">타임라인 추가</h3>
      <div class="input-group">
        <div class="time-input">
          <select v-model="newEvent.hours" class="time-select" aria-label="시간">
            <option v-for="hour in 24" :key="hour - 1" :value="(hour - 1).toString().padStart(2, '0')">
              {{ (hour - 1).toString().padStart(2, "0") }}
            </option>
          </select>
          <span class="time-separator">:</span>
          <select v-model="newEvent.minutes" class="time-select" aria-label="분">
            <option v-for="minute in 60" :key="minute - 1" :value="(minute - 1).toString().padStart(2, '0')">
              {{ (minute - 1).toString().padStart(2, "0") }}
            </option>
          </select>
        </div>
        <input type="text" v-model="newEvent.title" placeholder="이 시간엔 어떤 일이 있었나요?" class="title-input" required />
        <button @click="addTimelineEvent" class="add-event-btn" :disabled="!newEvent.title.trim()">
          <i class="fas fa-plus"></i>
          추가
        </button>
      </div>
    </div>

    <!-- 타임라인 목록 -->
    <div class="timeline-container">
      <div v-if="!sortedTimelineEvents.length" class="empty-state">
        <i class="fas fa-clock empty-icon"></i>
        <p>아직 타임라인이 없습니다. 첫 번째 타임라인을 추가해보세요!</p>
      </div>

      <div v-else v-for="event in sortedTimelineEvents" :key="event.id" class="timeline-event" :class="{ 'fade-enter': event.isNew }">
        <div class="event-time">
          <span class="time">{{ event.time }}</span>
          <div class="time-indicator"></div>
        </div>

        <div class="event-card">
          <div class="event-content">
            <h4>{{ event.title }}</h4>
            <p v-if="event.description">{{ event.description }}</p>
          </div>

          <button @click="deleteTimelineEvent(event.id)" class="delete-event-btn" aria-label="타임라인 삭제">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const route = useRoute();

// 상태 관리
const timelineEvents = ref([]);
const newEvent = ref({
  hours: "00",
  minutes: "00",
  title: "",
});

// 시간순 정렬
const sortedTimelineEvents = computed(() => {
  return [...timelineEvents.value].sort((a, b) => {
    return a.time.localeCompare(b.time);
  });
});

// 현재 유저 확인
const isCurrentUser = (userId) => {
  return store.currentUser?.id === userId;
};

// 타임라인 데이터 조회
const getTimelineEvent = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    if (response.data.timeline) {
      timelineEvents.value = response.data.timeline;
    }
  } catch (error) {
    console.error("타임라인 조회 실패:", error);
  }
};

// 타임라인 추가
const addTimelineEvent = async () => {
  if (!newEvent.value.title.trim()) return;

  const formattedTime = `${newEvent.value.hours}:${newEvent.value.minutes}`;

  try {
    const response = await axios({
      method: "post",
      url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/timeline/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
      data: {
        time: formattedTime,
        title: newEvent.value.title,
      },
    });

    // 새로운 이벤트에 애니메이션 적용을 위한 플래그 추가
    timelineEvents.value = response.data.map((event) => ({
      ...event,
      isNew: event.time === formattedTime && event.title === newEvent.value.title,
    }));

    // 입력 폼 초기화
    newEvent.value = {
      hours: "00",
      minutes: "00",
      title: "",
    };

    // 애니메이션 플래그 제거
    setTimeout(() => {
      timelineEvents.value = timelineEvents.value.map((event) => ({
        ...event,
        isNew: false,
      }));
    }, 300);
  } catch (error) {
    console.error("타임라인 추가 실패:", error);
  }
};

// 타임라인 삭제
const deleteTimelineEvent = async (eventId) => {
  if (!confirm("이 타임라인을 삭제하시겠습니까?")) return;

  try {
    await axios({
      method: "delete",
      url: `${store.API_URL}/api/v1/group/movie/timeline/${eventId}/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    await getTimelineEvent();
  } catch (error) {
    console.error("타임라인 삭제 실패:", error);
  }
};

onMounted(() => {
  getTimelineEvent();
});
</script>

<style scoped>
.timeline-section {
  padding: 1rem 0;
}

/* 입력 폼 스타일 */
.timeline-form-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.input-group {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.time-input {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  padding: 0.5rem 0.8rem;
  border-radius: 8px;
  border: 1px solid #e1e1e1;
}

.time-select {
  background: transparent;
  border: none;
  color: #333;
  font-size: 1rem;
  padding: 0.3rem;
  width: 45px;
  -webkit-appearance: none;
  appearance: none;
  cursor: pointer;
  text-align: center;
}

.time-select:focus {
  outline: none;
}

.time-separator {
  color: #333;
  font-weight: 500;
  margin: 0 0.2rem;
}

.title-input {
  flex: 1;
  padding: 0.8rem 1rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  font-size: 0.95rem;
  background: #f8f9fa;
  transition: all 0.2s ease;
}

.title-input:focus {
  outline: none;
  border-color: #dc3545;
  background: white;
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
}

.add-event-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-event-btn:hover:not(:disabled) {
  background: #c82333;
  transform: translateY(-1px);
}

.add-event-btn:disabled {
  background: #e9ecef;
  cursor: not-allowed;
}

/* 타임라인 목록 스타일 */
.timeline-container {
  position: relative;
  padding-left: 2rem;
}

.timeline-container::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e9ecef;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: #6c757d;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.timeline-event {
  position: relative;
  margin-bottom: 1.5rem;
  opacity: 1;
  transform: translateX(0);
  transition: all 0.3s ease;
}

.timeline-event.fade-enter {
  opacity: 0;
  transform: translateX(20px);
}

.event-time {
  position: absolute;
  left: -2rem;
  display: flex;
  align-items: center;
  transform: translateX(-100%);
  padding-right: 1rem;
}

.time {
  font-size: 0.9rem;
  font-weight: 500;
  color: #495057;
  white-space: nowrap;
}

.time-indicator {
  position: relative;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #dc3545;
  margin-left: 1rem;
  z-index: 1;
}

.time-indicator::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(220, 53, 69, 0.2);
  z-index: -1;
}

.event-card {
  position: relative;
  background: white;
  border-radius: 12px;
  padding: 1.2rem;
  margin-left: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.event-content {
  flex: 1;
  padding-right: 2rem; /* 삭제 버튼을 위한 공간 확보 */
}

.event-card:hover {
  transform: translateY(-2px);
}

.event-content h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.event-content p {
  margin: 0.5rem 0 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
}

.delete-event-btn {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  padding: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.timeline-event:hover .delete-event-btn {
  opacity: 1;
}

.delete-btn:hover {
  opacity: 1;
  transform: scale(1.1);
}
.timeline-event .delete-btn {
  opacity: 0; /* 기본적으로는 숨김 */
}
.timeline-event:hover .delete-btn {
  opacity: 1; /* hover시 보이게 */
}

@media (max-width: 768px) {
  .timeline-section {
    padding: 1rem;
  }

  .input-group {
    flex-direction: column;
  }

  .time-input {
    width: 100%;
  }

  .add-event-btn {
    width: 100%;
  }

  .timeline-container {
    padding-left: 1.5rem;
  }

  .event-time {
    left: -1.5rem;
  }

  .timeline-event .delete-btn {
    opacity: 0.7; /* 모바일에서는 항상 보이게 */
  }
  .delete-btn {
    opacity: 0.7; /* 모바일에서는 항상 표시 */
    padding: 0.8rem; /* 터치 영역 확대 */
  }
}
</style>
