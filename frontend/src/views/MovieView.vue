<template>
  <div>
    <h1>Movie page</h1>

    <!-- 검색창 -->
    <!-- 검색창을 눌렀을 때 모달창을 띄우는게 필요하니까 버튼임 -->
    <div>
      <button type="button" @click="openModal" class="search-btn">영화 제목을 입력해주세요.</button>
    </div>
    <SearchModal :is-open="isModalOpen" @close="closeModal" />
    <br />

    <h2>박스오피스 순위</h2>
    <div class="movie-list">
      <MovieCard v-for="(movie, index) in populaMovies" :key="movie.id" :movie="movie" type="popular" :index="index" />
    </div>
    <br />

    <h2>현재 상영작</h2>
    <div class="movie-list">
      <MovieCard v-for="movie in nowPlayingMovies" :key="movie.id" :movie="movie" type="nowplaying" />
    </div>
    <br />

    <h2>개봉예정작</h2>
    <div class="movie-list">
      <MovieCard v-for="movie in upComingMovies" :key="movie.id" :movie="movie" type="upcoming" />
    </div>
  </div>
  <br />
</template>

<script setup>
import MovieCard from "@/components/MovieCard.vue";
import SearchModal from "@/components/SearchModal.vue";
import axios from "axios";
import { onMounted, ref } from "vue";

const populaMovies = ref([]);
const nowPlayingMovies = ref([]);
const upComingMovies = ref([]);

// const API_KEY =
//   "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YjI0YzA4NjJkNTQwODFmYjE0Y2VhZGMwMWZkODI4MCIsIm5iZiI6MTczMTY0NzQ1Ni42NDg5MzUzLCJzdWIiOiI2NzM2ZDc0MWZmZTM4NzhlOWU5ZmFmYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.eYQu1H6KBYqKX0e-WvHcWIH3AT1ioH1j-4OmFLxxUxk";

const API_KEY = import.meta.env.VITE_TMDB_API_KEY;

// 모달
const isModalOpen = ref(false);

const openModal = () => {
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

// 박스오피스 순위
const getPopularMovies = () => {
  axios({
    method: "get",
    url: "https://api.themoviedb.org/3/movie/popular?language=ko-KR&region=KR&page=1",
    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      console.log("response = ", response);
      populaMovies.value = response.data.results;
    })
    .catch((error) => {
      console.log("error = ", error);
    });
};

// 현재상영작
const getnowPlayingMovies = () => {
  axios({
    method: "get",
    url: "https://api.themoviedb.org/3/movie/now_playing?language=ko-KR&region=KR&page=1",

    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      console.log("response = ", response);
      nowPlayingMovies.value = response.data.results;
    })
    .catch((error) => {
      console.log("error = ", error);
    });
};

// 개봉예정작
const getupComingMovies = () => {
  axios({
    method: "get",
    url: "https://api.themoviedb.org/3/movie/upcoming?language=ko-KR&page=1",

    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      console.log("response = ", response);
      upComingMovies.value = response.data.results;
    })
    .catch((error) => {
      console.log("error = ", error);
    });
};

onMounted(() => {
  getPopularMovies(), getnowPlayingMovies(), getupComingMovies();
});
</script>

<style scoped>
/* 영화 */
.movie-list {
  display: flex;
  gap: 20px;
  overflow-x: scroll;
  padding: 20px 0;
}

/* 검색모달 */
.search-btn {
  width: 1000px;
  height: 50px;
  border-style: none;
  position: center;
  border-radius: 10px;
  text-align: left;
  display: block; /* 추가 */
  margin: 50px auto; /* 상하 여백 30px, 가운데 정렬 */
  background-color: #f5f5f5;
  cursor: pointer; /* 마우스 오버시 포인터 변경 */
}
</style>
