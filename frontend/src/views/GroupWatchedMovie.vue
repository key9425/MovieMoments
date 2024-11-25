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
        <router-link
          v-for="tab in tabs"
          :key="tab.route"
          :to="{
            name: tab.route,
            params: {
              group_id: route.params.group_id,
              group_movie_id: route.params.group_movie_id,
            },
          }"
          class="tab-button"
          :class="{ active: route.name === tab.route }"
        >
          {{ tab.name }}
        </router-link>
      </div>
    </nav>

    <!-- 탭 컨텐츠 -->
    <main v-if="movie" class="main-content">
      <router-view
        :timeline-data="movie.timeline"
        :one-line-review-data="movie.review"
        :articles-data="movie.article"
        :gallery-data="movie.article_img"
        @update:articles-images="updateArticlesImages"
      />
    </main>

    <!-- 채팅 패널 -->
    <!-- <div class="chat-panel" :class="{ expanded: isChatExpanded }">
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
    </div> -->
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import ArticleModal from "@/components/ArticleModal.vue";
import Timeline from "@/components/GroupWatchedMovie/Timeline.vue";
import OneLineReview from "@/components/GroupWatchedMovie/OneLineReview.vue";
import Article from "@/components/GroupWatchedMovie/Article.vue";
import Gallery from "@/components/GroupWatchedMovie/Gallery.vue";

const route = useRoute();
const heroSection = ref(null);
const tabNav = ref(null);
const isTabSticky = ref(false);
const isChatExpanded = ref(false);
const newMessage = ref("");
const store = useCounterStore();
const chatMessages = ref([]);
const movie = ref(null);
const currentUserId = ref("user1");

// 탭 정의
const tabs = [
  { route: "MovieTimeline", name: "타임라인" },
  { route: "MovieReviews", name: "한줄평" },
  { route: "MovieArticles", name: "게시글" },
  { route: "MovieGallery", name: "갤러리" },
];

const updateArticlesImages = (newImages) => {
  if (!movie.value) return;

  movie.value = {
    ...movie.value,
    article_img: [...movie.value.article_img, ...newImages],
  };
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
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("getGroupWatchedMovie", response.data);
      movie.value = response.data;
    })
    .catch((error) => {
      console.log(error.response.data);
    });
};

onMounted(() => {
  getGroupWatchedMovie();
});
</script>

<style scoped>
/* 기존 스타일 유지 */
.page-container {
  min-height: 100vh;
  background-color: #ffffff;
  color: #333333;
}

.header-actions {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 1000;
}

.create-article-btn {
  background: rgba(255, 255, 255, 0.9);
  color: #333333;
  border: 1px solid #e1e1e1;
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
  background: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

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

.backdrop-wrapper img {
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
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.8) 60%, #ffffff 100%);
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
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.movie-details {
  flex-grow: 1;
}

.movie-title {
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #1a1a1a;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.movie-meta {
  font-size: 1.1rem;
  color: rgba(0, 0, 0, 0.7);
}

.divider {
  margin: 0 0.5rem;
  color: rgba(0, 0, 0, 0.3);
}

/* 탭 네비게이션 스타일 업데이트 */
.tab-navigation {
  background: #ffffff;
  padding: 1rem 0;
  transition: all 0.3s ease;
  border-bottom: 1px solid #e1e1e1;
}

.tab-navigation.sticky {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.tab-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 5%;
  display: flex;
  gap: 2rem;
}

/* router-link 스타일링 */
.tab-button {
  background: none;
  border: none;
  color: rgba(0, 0, 0, 0.6);
  font-size: 1.1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none; /* 밑줄 제거 */
  display: inline-block;
}

.tab-button.active {
  color: #3a3a3a;
  border-bottom: 2px solid #3a3a3a;
}

/* 나머지 스타일 유지 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 5%;
}

.chat-panel {
  position: fixed;
  bottom: 0;
  right: 2rem;
  width: 350px;
  background: #ffffff;
  border-radius: 12px 12px 0 0;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: transform 0.3s ease;
}

.chat-header {
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e1e1e1;
  border-radius: 12px 12px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
  color: #333333;
}

.toggle-icon {
  opacity: 0.7;
}

.chat-content {
  height: 400px;
  display: flex;
  flex-direction: column;
  border: 1px solid #e1e1e1;
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
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 0.2rem;
}

.message-bubble {
  background: #f0f2f5;
  padding: 0.8rem 1rem;
  border-radius: 1rem;
  color: #333333;
}

.message-mine .message-bubble {
  background: #3a3a3a;
  color: white;
}

.message-time {
  font-size: 0.7rem;
  color: rgba(0, 0, 0, 0.4);
  margin-top: 0.2rem;
}

.chat-input {
  padding: 1rem;
  display: flex;
  gap: 0.5rem;
  background: #f8f9fa;
  border-top: 1px solid #e1e1e1;
}

.chat-input input {
  flex-grow: 1;
  padding: 0.8rem 1rem;
  border-radius: 20px;
  border: 1px solid #e1e1e1;
  background: #ffffff;
  color: #333333;
  font-size: 0.9rem;
}

.chat-input input:focus {
  outline: none;
  border-color: #3a3a3a;
  box-shadow: 0 0 0 2px rgba(41, 128, 185, 0.2);
}

.chat-input button {
  padding: 0.8rem 1.2rem;
  border-radius: 20px;
  border: none;
  background: #3a3a3a;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.chat-input button:hover {
  background: #2471a3;
}

.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

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
    background: #ffffff;
  }

  .chat-content {
    height: 350px;
  }

  .create-article-btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
