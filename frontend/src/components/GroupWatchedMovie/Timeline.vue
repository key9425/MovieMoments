<template>
  <!-- 타임라인 탭 -->
  <section v-if="currentTab === 'timeline'" class="timeline-section">
    <!-- timelineEvents를 시간순으로 정렬(sortedTimelineEvents)한 걸 v-for로 하나씩 event -->
    <div class="timeline-event" v-for="event in sortedTimelineEvents" :key="event.time">
      <div class="event-time">{{ event.time }}</div>
      <div class="event-content">
        <h5>{{ event.title }}</h5>
        <p v-if="event.description">{{ event.description }}</p>
      </div>
    </div>

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
//=====================================================================

// 사용자가 기존에 입력한 타임라인 데이터 채워질 곳
const timelineEvents = ref([]);

// 시간순서대로 표시되도록 정렬
const sortedTimelineEvents = computed(() => {
  return [...timelineEvents.value].sort((a, b) => {
    return a.time.localeCompare(b.time);
  });
});

// 기존에 작성한 데이터 받아오기
// 아래 형식으로 받아오게끔 요청
// const timelineEvents = ref([
//   { time: "17:30", title: "영화관 도착! 다같이 모였어요 🎬" },
//   { time: "18:00", title: "팝콘 먹으면서 영화 시작 전 수다 타임 🍿" },
//   { time: "18:30", title: "영화 시작! 🎥" },
// ]);
const getTimelineEvent = () => {
  axios({
    method: "get",
    // url: `타임라인 요청 url`,
    url: `${store.API_URL}/api/v1/groups/movie/${route.params.group_movie_id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("onMount 응답 결과 : ");
      console.log(response);
      timelineEvents.value = response.data;
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
  // 내용이 없다면 서버에 보내지 않겠다.
  if (!newEvent.value.title) return;

  // 타임라인에 타임에 "17:30"으로 들어가게
  const formattedTime = `${newEvent.value.hours}:${newEvent.value.minutes}`;

  axios({
    method: "post",
    // url: `타임라인 요청 url`,
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
</style>
