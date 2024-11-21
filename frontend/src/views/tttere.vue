<template>
  <div v-if="movie">
    <div class="position-relative movie-backdrop mb-4">
      <!-- 백드롭 이미지 -->
      <img :src="`https://image.tmdb.org/t/p/original/${movie.backdrop_path}`" :alt="movie.title" class="w-100" />
      <!-- 영화 정보 오버레이 -->
      <div class="movie-info-overlay">
        <div class="container">
          <!-- 제목 -->
          <h1 class="display-4 text-white mb-2">{{ movie.title }}</h1>
          <div class="d-flex flex-wrap align-items-center text-white gap-3"></div>
          <span>{{ movie.runtime }}분</span>
          <span>•</span>
          <span>{{ movie.genres?.map((genre) => genre.name).join(", ") }}</span>
        </div>
      </div>
    </div>

    <!-- 좌측 영화 포스터 -->
    <div class="container">
      <div class="row">
        <div class="col-md-4 mb-4">
          <div style="width: 18rem">
            <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" class="card-img-top" alt="..." />
            <button>찜하기</button>
          </div>
        </div>
      </div>

      <!--  우측 줄거리 -->
      <div class="col-md-8">
        <div class="card mb-4">
          <div class="card-header">
            <h2 class="h5 mb-0">작품 정보</h2>
          </div>
          <div class="card-body">
            <p class="card-text">{{ movie.overview }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const movie = ref(null);
const movieId = route.params.movieId;

const API_KEY =
  "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YjI0YzA4NjJkNTQwODFmYjE0Y2VhZGMwMWZkODI4MCIsIm5iZiI6MTczMTY0NzQ1Ni42NDg5MzUzLCJzdWIiOiI2NzM2ZDc0MWZmZTM4NzhlOWU5ZmFmYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.eYQu1H6KBYqKX0e-WvHcWIH3AT1ioH1j-4OmFLxxUxk";

// 영화 디테일 정보
const getMovieDetails = () => {
  axios({
    method: "get",
    url: `https://api.themoviedb.org/3/movie/${movieId}`,
    params: {
      language: "ko-KR",
    },
    headers: {
      accept: "application/json",
      Authorization: API_KEY,
    },
  })
    .then((response) => {
      console.log("response = ", response);
      movie.value = response.data;
    })
    .catch((error) => {
      console.log("error = ", error);
    });
};

onMounted(() => {
  getMovieDetails();
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
