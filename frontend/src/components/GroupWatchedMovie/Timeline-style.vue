<template>
  <!-- 타임라인 탭 -->
  <section v-if="currentTab === 'timeline'" class="timeline-section">
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
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const props = defineProps(["currentTab"]);
const store = useCounterStore();
const route = useRoute();

// 사용자가 기존에 입력한 타임라인 데이터 채워질 곳
const timelineEvents = ref([]);

// 시간순서대로 표시되도록 정렬
const sortedTimelineEvents = computed(() => {
  return [...timelineEvents.value].sort((a, b) => {
    return a.time.localeCompare(b.time);
  });
});

// 기존에 작성한 데이터 받아오기
const getTimelineEvent = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("onMount 응답 결과 : ");
      console.log(response);
      timelineEvents.value = response.data.timeline;
    })
    .catch((error) => {
      console.log(error);
      console.log("타임라인 받아오기 실패");
    });
};

// 입력폼에 작성한 내용인 newEvent에 저장
const newEvent = ref({
  hours: "00",
  minutes: "00",
  title: "",
});

// 새로 타임라인 등록에 대한 요청
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
      console.log(response.data);
      timelineEvents.value = response.data;
      // 입력 폼 초기화
      newEvent.value = {
        hours: "00",
        minutes: "00",
        title: "",
      };
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  getTimelineEvent();
});
</script>

<style scoped>
/* 타임라인 섹션 전체 스타일 */
.timeline-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 1rem;
  position: relative;
}

/* 타임라인 입력 폼 */
.timeline-input-form {
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.input-group {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* 시간 선택 input */
.custom-time-input {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  gap: 0.25rem;
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
  color: #666;
  font-weight: 500;
}

/* 제목 입력 input */
.title-input {
  flex-grow: 1;
  padding: 0.875rem 1.25rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  background: #f8f9fa;
}

.title-input:focus {
  outline: none;
  border-color: #3a3a3a;
  background: white;
}

/* 등록 버튼 */
.add-event-btn {
  padding: 0.875rem 1.5rem;
  border-radius: 4px;
  border: none;
  background: #3a3a3a;
  color: white;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  min-width: 100px;
}

.add-event-btn:hover {
  background: #2a2a2a;
}

/* 타임라인 이벤트 항목 */
.timeline-event {
  display: flex;
  position: relative;
  padding: 1.5rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-left: 7rem;
}

.timeline-event::before {
  content: "";
  position: absolute;
  left: -3rem;
  top: 50%;
  width: 3rem;
  height: 1px;
  background: #ddd;
}

.event-time {
  position: absolute;
  left: -7rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  font-weight: 500;
  color: #666;
  background: white;
  padding: 0.5rem 0;
  width: 80px;
  text-align: right;
}

.event-content {
  flex: 1;
}

.event-content h5 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
  display: flex;
  align-items: center;
}

.event-content p {
  margin: 0.75rem 0 0;
  font-size: 1rem;
  color: #666;
  line-height: 1.5;
}

/* 타임라인 연결선 */
.timeline-section::before {
  content: "";
  position: absolute;
  left: 6rem;
  top: 8.5rem;
  bottom: 0;
  width: 1px;
  background: #ddd;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .timeline-event {
    margin-left: 4rem;
  }

  .event-time {
    left: -4.5rem;
    width: 60px;
    font-size: 1rem;
  }

  .timeline-section::before {
    left: 3.5rem;
  }

  .input-group {
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .custom-time-input {
    flex: 0 0 auto;
  }

  .title-input {
    flex: 1 1 200px;
  }

  .add-event-btn {
    width: 100%;
  }
}
</style>
