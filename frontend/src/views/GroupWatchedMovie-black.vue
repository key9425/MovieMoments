<template>
  <div class="page-container">
    <ArticleModal ref="articleModal" @submit="handleSubmit" :id="route.params.group_movie_id" />

    <!-- 영화 정보 섹션 -->
    <section class="hero-section" ref="heroSection">
      <div v-if="movie" class="backdrop-wrapper">
        <img :src="`https://image.tmdb.org/t/p/original/${movie.movie.backdrop_path}`" :alt="movie.movie.title" />
        <div class="backdrop-overlay"></div>
      </div>

      <div v-if="movie" class="movie-info">
        <!-- 포스터 -->
        <div class="poster-container">
          <img :src="`https://image.tmdb.org/t/p/w500/${movie.movie.poster_path}`" :alt="movie.movie.title" class="movie-poster" />
        </div>

        <div class="movie-details">
          <h1 class="movie-title">{{ movie.movie.title }}</h1>
          <div class="movie-meta">
            <span>{{ new Date(movie.movie.release_date).getFullYear() }}</span>
            <span class="divider">•</span>
            <span>{{ movie.movie.runtime }}분</span>
            <span class="divider">•</span>
            <span>{{ movie.genres?.map((genre) => genre.name).join(", ") }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 탭 네비게이션 -->
    <nav class="tab-navigation" :class="{ sticky: isTabSticky }" ref="tabNav">
      <div class="tab-container">
        <button v-for="tab in tabs" :key="tab.id" :class="['tab-button', { active: currentTab === tab.id }]" @click="currentTab = tab.id">
          {{ tab.name }}
        </button>
      </div>
    </nav>

    <!-- 탭 컨텐츠 -->
    <main class="main-content">
      <!-- 타임라인 탭 -->
      <section v-if="currentTab === 'timeline'" class="timeline-section">
        <div class="timeline-event" v-for="event in timelineEvents" :key="event.time">
          <div class="event-time">{{ event.time }}</div>
          <div class="event-content">
            <h5>{{ event.title }}</h5>
            <p v-if="event.description">{{ event.description }}</p>
          </div>
        </div>
      </section>

      <!-- 한줄평 탭 -->
      <section v-if="currentTab === 'reviews'" class="reviews-section">
        <div class="review-card" v-for="review in reviews" :key="review.id">
          <div class="review-header">
            <div class="user-info">
              <img :src="review.userProfile" :alt="review.userName" class="user-avatar" />
              <span class="user-name">{{ review.userName }}</span>
            </div>
            <span class="review-date">{{ review.date }}</span>
          </div>
          <p class="review-text">{{ review.content }}</p>
        </div>
      </section>

      <!-- 갤러리 탭 -->
      <section v-if="currentTab === 'gallery'" class="gallery-section">
        <div class="gallery-grid">
          <div v-for="image in galleryImages" :key="image.id" class="gallery-item" @click="openImage(image)">
            <img :src="image.url" :alt="image.description" />
          </div>
        </div>
      </section>
    </main>

    <!-- 채팅 패널 -->
    <div class="chat-panel" :class="{ expanded: isChatExpanded }">
      <div class="chat-header" @click="toggleChat">
        <span>채팅</span>
        <span class="toggle-icon">{{ isChatExpanded ? "▼" : "▲" }}</span>
      </div>

      <div class="chat-content" v-if="isChatExpanded">
        <div class="messages-container" ref="chatMessages">
          <div v-for="message in chatMessages" :key="message.id" :class="['message', message.userId === currentUserId ? 'message-mine' : 'message-other']">
            <span class="message-author">{{ message.userName }}</span>
            <div class="message-bubble">{{ message.content }}</div>
            <span class="message-time">{{ message.time }}</span>
          </div>
        </div>

        <div class="chat-input">
          <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="메시지를 입력하세요..." />
          <button @click="sendMessage">전송</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import ArticleModal from "@/components/ArticleModal.vue";

const route = useRoute();
import axios from "axios";
const heroSection = ref(null);
const tabNav = ref(null);
const isTabSticky = ref(false);
const currentTab = ref("timeline");
const isChatExpanded = ref(false);
const newMessage = ref("");
const store = useCounterStore();
const chatMessages = ref([]);
const movie = ref(null);
const currentUserId = ref("user1");

// 탭 정의
const tabs = [
  { id: "timeline", name: "타임라인" },
  { id: "reviews", name: "한줄평" },
  { id: "gallery", name: "갤러리" },
];

// 샘플 데이터
const timelineEvents = ref([
  { time: "17:30", title: "영화관 도착! 다같이 모였어요 🎬" },
  { time: "18:00", title: "팝콘 먹으면서 영화 시작 전 수다 타임 🍿" },
  { time: "18:30", title: "영화 시작! 🎥" },
]);

const reviews = ref([
  {
    id: 1,
    userName: "민지",
    userProfile: "/api/placeholder/40/40",
    content: "시간 가는 줄 몰랐어요! 플롯이 정말 탄탄해요.",
    date: "2024.03.15",
  },
]);

const galleryImages = ref([{ id: 1, url: "/api/placeholder/300/300", description: "Gallery image 1" }]);

// 스크롤 이벤트 핸들러
const handleScroll = () => {
  if (!heroSection.value || !tabNav.value) return;

  const heroHeight = heroSection.value.offsetHeight;
  const scrollPosition = window.scrollY;

  isTabSticky.value = scrollPosition > heroHeight - tabNav.value.offsetHeight;
};

// 채팅 기능
const toggleChat = () => {
  isChatExpanded.value = !isChatExpanded.value;
};

const sendMessage = () => {
  if (!newMessage.value.trim()) return;

  chatMessages.value.push({
    id: Date.now(),
    userId: currentUserId.value,
    userName: "나",
    content: newMessage.value,
    time: new Date().toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" }),
  });

  newMessage.value = "";

  // 스크롤을 최신 메시지로 이동
  setTimeout(() => {
    const chatMessagesEl = document.querySelector(".messages-container");
    if (chatMessagesEl) {
      chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
    }
  }, 0);
};

const getGroupWatchedMovie = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/groups/${route.params.group_movie_id}/articles/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response.data);
      movie.value = response.data.group_movie;
    })
    .catch((error) => {
      console.log(error.response.data);
    });
};

// 컴포넌트 라이프사이클 훅
onMounted(() => {
  getGroupWatchedMovie();
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  background-color: #141414;
  color: white;
}

/* 헤더 스타일 */
.header-actions {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 1000;
}

.create-article-btn {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-article-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* 히어로 섹션 스타일 */
.hero-section {
  position: relative;
  height: 100vh;
  overflow: hidden;
}

.backdrop-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.backdrop-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.backdrop-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(20, 20, 20, 0.2) 0%, rgba(20, 20, 20, 0.8) 60%, #141414 100%);
}

.movie-info {
  position: absolute;
  bottom: 10%;
  left: 0;
  width: 100%;
  padding: 0 5%;
  display: flex;
  align-items: flex-end;
  gap: 2rem;
}

.poster-container {
  flex-shrink: 0;
}

.movie-poster {
  width: 300px;
  border-radius: 12px;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
}

.movie-details {
  flex-grow: 1;
}

.movie-title {
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.movie-meta {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
}

.divider {
  margin: 0 0.5rem;
  color: rgba(255, 255, 255, 0.4);
}

/* 탭 네비게이션 스타일 */
.tab-navigation {
  background: #141414;
  padding: 1rem 0;
  transition: all 0.3s ease;
}

.tab-navigation.sticky {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(20, 20, 20, 0.95);
  backdrop-filter: blur(10px);
}

.tab-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 5%;
  display: flex;
  gap: 2rem;
}

.tab-button {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-button.active {
  color: white;
  border-bottom: 2px solid #3498db;
}

/* 메인 컨텐츠 스타일 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 5%;
}

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
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.event-time {
  flex-shrink: 0;
  font-size: 1.2rem;
  color: #3498db;
  width: 80px;
}

/* 리뷰 스타일 */
.reviews-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.review-date {
  color: rgba(255, 255, 255, 0.6);
}

/* 갤러리 스타일 */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.gallery-item {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 12px;
  cursor: pointer;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

/* 채팅 패널 스타일 */
/* 채팅 패널 스타일 */
.chat-panel {
  position: fixed;
  bottom: 0;
  right: 2rem;
  width: 350px;
  background: #1a1a1a;
  border-radius: 12px 12px 0 0;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  transition: transform 0.3s ease;
}

.chat-header {
  padding: 1rem;
  background: #2c2c2c;
  border-radius: 12px 12px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.toggle-icon {
  opacity: 0.7;
}

.chat-content {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.messages-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.message-mine {
  align-self: flex-end;
  align-items: flex-end;
}

.message-other {
  align-self: flex-start;
  align-items: flex-start;
}

.message-author {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.2rem;
}

.message-bubble {
  background: #2c2c2c;
  padding: 0.8rem 1rem;
  border-radius: 1rem;
  color: white;
}

.message-mine .message-bubble {
  background: #3498db;
}

.message-time {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 0.2rem;
}

.chat-input {
  padding: 1rem;
  display: flex;
  gap: 0.5rem;
  background: #2c2c2c;
}

.chat-input input {
  flex-grow: 1;
  padding: 0.8rem 1rem;
  border-radius: 20px;
  border: none;
  background: #1a1a1a;
  color: white;
  font-size: 0.9rem;
}

.chat-input input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.5);
}

.chat-input button {
  padding: 0.8rem 1.2rem;
  border-radius: 20px;
  border: none;
  background: #3498db;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.chat-input button:hover {
  background: #2980b9;
}

/* 반응형 스타일 */
@media (max-width: 1024px) {
  .movie-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 0 2rem;
  }

  .movie-poster {
    width: 200px;
  }

  .movie-title {
    font-size: 2.5rem;
  }

  .chat-panel {
    right: 1rem;
    width: 300px;
  }
}

@media (max-width: 768px) {
  .hero-section {
    height: 70vh;
  }

  .movie-title {
    font-size: 2rem;
  }

  .tab-container {
    padding: 0 1rem;
  }

  .main-content {
    padding: 1rem;
  }

  .chat-panel {
    right: 0;
    width: 100%;
  }

  .chat-content {
    height: 350px;
  }

  .create-article-btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}

/* 스크롤바 스타일링 */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

.messages-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
