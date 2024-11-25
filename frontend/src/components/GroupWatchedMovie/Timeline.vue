<template>
  <section class="timeline-section">
    <!-- 타임라인 입력 폼 -->
    <div class="timeline-input-form">
      <div class="input-group">
        <div class="custom-time-input">
          <select v-model="newEvent.hours" class="time-select">
            <option v-for="hour in 24" :key="hour - 1" :value="(hour - 1).toString().padStart(2, '0')">
              {{ (hour - 1).toString().padStart(2, "0") }}
            </option>
          </select>
          <span class="time-separator">:</span>
          <select v-model="newEvent.minutes" class="time-select">
            <option v-for="minute in 60" :key="minute - 1" :value="(minute - 1).toString().padStart(2, '0')">
              {{ (minute - 1).toString().padStart(2, "0") }}
            </option>
          </select>
        </div>
        <input type="text" v-model="newEvent.title" placeholder="하루에 대한 기록을 남겨주세요." class="title-input" required />
        <button @click="addTimelineEvent" class="add-event-btn">등록</button>
      </div>
    </div>

    <!-- 타임라인 이벤트 표시 -->
    <div class="timeline-event" v-for="event in sortedTimelineEvents" :key="event.time">
      <div class="event-time">{{ event.time }}</div>
      <div class="event-content">
        <h5>{{ event.title }}</h5>
        <p v-if="event.description">{{ event.description }}</p>
      </div>
      <!-- 삭제 버튼 -->
      <button @click="deleteTimelineEvent(event.id)" class="delete-event-btn">
        <i class="fas fa-times"></i>
      </button>
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

// 타임라인 데이터 초기화
const timelineEvents = ref([]);

// 시간순 정렬
const sortedTimelineEvents = computed(() => {
  return [...timelineEvents.value].sort((a, b) => {
    return a.time.localeCompare(b.time);
  });
});

// 데이터 가져오기
const getTimelineEvent = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      if (response.data.timeline) {
        timelineEvents.value = response.data.timeline;
      }
    })
    .catch((error) => {
      console.log("타임라인 받아오기 실패:", error);
    });
};

// 새 이벤트 상태
const newEvent = ref({
  hours: "00",
  minutes: "00",
  title: "",
});

// 타임라인 추가
const addTimelineEvent = () => {
  if (!newEvent.value.title) return;

  const formattedTime = `${newEvent.value.hours}:${newEvent.value.minutes}`;

  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/timeline/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: {
      time: formattedTime,
      title: newEvent.value.title,
    },
  })
    .then((response) => {
      timelineEvents.value = response.data;
      // 입력 폼 초기화
      newEvent.value = {
        hours: "00",
        minutes: "00",
        title: "",
      };
    })
    .catch((error) => {
      console.log("타임라인 추가 실패:", error);
    });
};

// 타임라인 삭제
const deleteTimelineEvent = (eventId) => {
  if (!confirm("정말 이 타임라인을 삭제하시겠습니까?")) return;

  axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/group/movie/timeline/${eventId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      getTimelineEvent();
    })
    .catch((error) => {
      console.error("타임라인 삭제 실패:", error);
      alert("타임라인 삭제에 실패했습니다.");
    });
};

onMounted(() => {
  getTimelineEvent();
});
</script>

<style scoped>
/* 타임라인 스타일 */
.timeline-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  justify-content: center;
}

.timeline-event {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
}

.event-time {
  flex-shrink: 0;
  font-size: 1.2rem;
  color: #3a3a3a;
  width: 80px;
}

/* 입력 폼 스타일 수정 */
.timeline-input-form {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
}

.input-group {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.custom-time-input {
  display: flex;
  align-items: center;
  background: #ffffff;
  padding: 0.5rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  gap: 0.25rem;
}

.time-select {
  background: transparent;
  border: none;
  color: #333333;
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
  background-color: #f8f9fa;
}

.time-separator {
  color: #333333;
  font-weight: bold;
}

.title-input {
  flex-grow: 1;
  padding: 0.8rem;
  border-radius: 8px;
  border: 1px solid #e1e1e1;
  background: #ffffff;
  color: #333333;
}

.title-input:focus {
  outline: none;
  border-color: #3a3a3a;
  box-shadow: 0 0 0 2px rgba(41, 128, 185, 0.1);
}

.add-event-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  border: none;
  background: #3a3a3a;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-event-btn:hover {
  background: #2471a3;
  transform: translateY(-1px);
}

.add-event-btn:active {
  transform: translateY(0);
}
.timeline-event {
  position: relative; /* 삭제 버튼의 위치 기준점 */
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

.delete-event-btn:hover {
  color: #c82333;
}

/* 모바일 대응을 위한 미디어 쿼리 */
@media (max-width: 768px) {
  .delete-event-btn {
    opacity: 1; /* 모바일에서는 항상 표시 */
    padding: 0.8rem; /* 터치 영역 확대 */
  }
}
</style>
