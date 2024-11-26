<template>
  <div class="page-container">
    <ArticleModal ref="articleModal" :id="route.params.group_movie_id" />

    <!-- 영화 히어로 섹션 -->
    <section class="movie-hero position-relative">
      <div v-if="movie" class="backdrop-wrapper">
        <img :src="`https://image.tmdb.org/t/p/original/${movie.movie.backdrop_path}`" :alt="movie.movie.title" class="backdrop-image" />
        <div class="backdrop-overlay"></div>
      </div>

      <div v-if="movie" class="hero-content container">
        <div class="row align-items-end">
          <div class="col-md-3">
            <img :src="`https://image.tmdb.org/t/p/w500/${movie.movie.poster_path}`" :alt="movie.movie.title" class="poster-image" />
          </div>
          <div class="col-md-9">
            <h1 class="movie-title text-white mb-3">{{ movie.movie.title }}</h1>
            <div class="movie-meta text-white mb-4">
              <span>{{ new Date(movie.movie.release_date).getFullYear() }}</span>
              <span class="meta-divider">•</span>
              <span>{{ movie.movie.runtime }}분</span>
              <span>{{ movie.genres?.map((genre) => genre.name).join(", ") }}</span>
            </div>
            <div class="d-flex align-items-center gap-4">
              <div class="rating">
                <i class="fas fa-star text-warning me-2"></i>
                <span class="text-white">{{ movie.movie.vote_average?.toFixed(1) }}</span>
              </div>
            </div>
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
// import Timeline from "@/components/GroupWatchedMovie/Timeline.vue";
// import OneLineReview from "@/components/GroupWatchedMovie/OneLineReview.vue";
// import Article from "@/components/GroupWatchedMovie/Article.vue";
// import Gallery from "@/components/GroupWatchedMovie/Gallery.vue";

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

const tabs = [
  { route: "MovieTimeline", name: "타임라인" },
  { route: "MovieReviews", name: "한줄평" },
  { route: "MovieArticles", name: "게시글" },
  { route: "MovieGallery", name: "갤러리" },
];

// 게시글 이미지 업데이트
const updateArticlesImages = (newImages) => {
  if (!movie.value) return;
  movie.value = {
    ...movie.value,
    article_img: [...movie.value.article_img, ...newImages],
  };
};

// 채팅기능
// const toggleChat = () => {
//   isChatExpanded.value = !isChatExpanded.value;
// };

// const sendMessage = () => {
//   if (!newMessage.value.trim()) return;

//   chatMessages.value.push({
//     id: Date.now(),
//     userId: currentUserId.value,
//     userName: "나",
//     content: newMessage.value,
//     time: new Date().toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" }),
//   });

//   newMessage.value = "";

//   setTimeout(() => {
//     const chatMessagesEl = document.querySelector(".messages-container");
//     if (chatMessagesEl) {
//       chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
//     }
//   }, 0);
// };

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
.page-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* 히어로 섹션 스타일 */
.movie-hero {
  height: 600px;
  position: relative;
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
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.8) 100%);
}

.hero-content {
  position: absolute;
  bottom: 3rem;
  left: 0;
  right: 0;
  z-index: 1;
}

.poster-image {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.movie-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.movie-meta {
  font-size: 1.1rem;
  opacity: 0.9;
}

.meta-divider {
  margin: 0 0.8rem;
  opacity: 0.6;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 0, 0, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  backdrop-filter: blur(4px);
}

/* 탭 네비게이션 스타일 */
.tab-navigation {
  background: #ffffff;
  border-bottom: 1px solid #e1e1e1;
  transition: all 0.3s ease;
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
  padding: 0 2rem;
  display: flex;
  gap: 2rem;
}

.tab-button {
  padding: 1rem 0.5rem;
  color: #666666;
  text-decoration: none;
  font-weight: 500;
  position: relative;
  transition: all 0.3s ease;
}

.tab-button.active {
  color: #dc3545;
}

.tab-button.active::after {
  content: "";
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background: #dc3545;
}

/* 메인 컨텐츠 영역 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* 채팅 패널 스타일 */
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

/* 반응형 스타일 */
@media (max-width: 768px) {
  .movie-hero {
    height: auto;
    min-height: 400px;
  }

  .hero-content {
    position: relative;
    bottom: 0;
    padding: 2rem 1rem;
  }

  .movie-title {
    font-size: 2rem;
  }

  .tab-container {
    padding: 0 1rem;
    gap: 1rem;
  }

  .poster-image {
    margin-bottom: 1rem;
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
}
</style>
