<template>
  <div class="movie-detail-container">
    <div class="header-actions">
      <button @click="goArticleCreate" class="create-article-btn">
        <span class="btn-icon">+</span>
        게시글 작성하기
      </button>
    </div>

    <ArticleModal ref="articleModal" @submit="handleSubmit" :id="route.params.group_movie_id" />

    <div v-if="movie" class="movie-content">
      <!-- 백드롭 섹션 -->
      <div class="backdrop-section">
        <div class="backdrop-image">
          <img :src="`https://image.tmdb.org/t/p/original/${movie.movie.backdrop_path}`" :alt="movie.movie.title" />
          <!-- 그라디언트 오버레이 -->
          <div class="backdrop-overlay"></div>
        </div>

        <!-- 영화 정보 -->
        <div class="movie-info">
          <div class="info-container">
            <!-- 포스터 -->
            <div class="poster-container">
              <img :src="`https://image.tmdb.org/t/p/w500/${movie.movie.poster_path}`" :alt="movie.movie.title" class="movie-poster" />
            </div>

            <!-- 상세 정보 -->
            <div class="detail-container">
              <h1>{{ movie.movie.title }}</h1>
              <div class="movie-meta">
                <span>{{ new Date(movie.movie.release_date).getFullYear() }}</span>
                <span class="meta-divider">•</span>
                <span>{{ movie.movie.runtime }}분</span>
                <span class="meta-divider">•</span>
                <span class="genres">{{ movie.genres?.map((genre) => genre.name).join(", ") }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import ArticleModal from "@/components/ArticleModal.vue";

const articleModal = ref(null);
const store = useCounterStore();
const route = useRoute();
const router = useRouter();
const movie = ref(null);

const goArticleCreate = () => {
  if (articleModal.value) {
    articleModal.value.open();
  }
};

const handleSubmit = (formData) => {
  console.log(formData);
  if (articleModal.value) {
    articleModal.value.close();
  }
};

const getGroupWatchedMovie = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/groups/movie/${route.params.group_movie_id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response.data);
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
.movie-detail-container {
  min-height: 100vh;
  background-color: #141414;
  color: white;
}

.header-actions {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 100;
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

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.backdrop-section {
  position: relative;
  height: 100vh;
  width: 100%;
}

.backdrop-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.backdrop-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.backdrop-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(20, 20, 20, 0.2) 0%, rgba(20, 20, 20, 0.8) 60%, rgba(20, 20, 20, 1) 100%);
}

.movie-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 3rem;
}

.info-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 3rem;
  align-items: flex-end;
}

.poster-container {
  flex-shrink: 0;
}

.movie-poster {
  width: 300px;
  border-radius: 12px;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
}

.detail-container {
  flex-grow: 1;
}

.detail-container h1 {
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.movie-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
}

.meta-divider {
  color: rgba(255, 255, 255, 0.4);
}

.genres {
  color: rgba(255, 255, 255, 0.6);
}

/* 스켈레톤 로딩 효과 */
img {
  background-color: rgba(255, 255, 255, 0.1);
  transition: opacity 0.3s ease;
}

img[src] {
  background-color: transparent;
}
</style>
