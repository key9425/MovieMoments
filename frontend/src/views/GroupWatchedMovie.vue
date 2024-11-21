<template>
  <div>
    <h1>GroupWatchedMovie</h1>
    <button @click="goArticleCreate">게시글 생성</button>

    <div v-if="movie">
      <!-- 백드롭 이미지 섹션 (전체 폭) -->
      <div class="position-relative movie-backdrop mb-4">
        <img :src="`https://image.tmdb.org/t/p/original/${movie.movie.backdrop_path}`" :alt="movie.title" class="w-100" />

        <!-- 영화 정보 오버레이 -->
        <div class="movie-info-overlay">
          <div class="container">
            <h1 class="display-4 text-white mb-2">{{ movie.movie.title }}</h1>
            <div class="d-flex flex-wrap align-items-center text-white gap-3">
              <span>{{ new Date(movie.movie.release_date).getFullYear() }}</span>
              <span>•</span>
              <span>{{ movie.movie.runtime }}분</span>
              <span>•</span>
              <span>{{ movie.genres?.map((genre) => genre.name).join(", ") }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

const store = useCounterStore();
const route = useRoute();
const movie = ref(null);

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

const goArticleCreate = () => {};

onMounted(() => {
  getGroupWatchedMovie();
});
</script>

<style scoped>
.movie-backdrop {
  height: 600px;
  overflow: hidden;
  position: relative;
}

.movie-backdrop img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.2));
}

.movie-info-overlay {
  position: absolute;
  bottom: 2rem;
  left: 0;
  right: 0;
  padding: 1rem;
}

.gap-3 {
  gap: 1rem;
}

/* 이미지 로딩 중 스켈레톤 효과 */
img {
  min-height: 200px;
  background-color: #e9ecef;
}
</style>
