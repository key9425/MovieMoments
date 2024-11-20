<template>
  <div>
    <h1>Movie page</h1>
    <form>
      <input type="text" placeholder="영화검색" />
    </form>
    <br />
    <h2>박스오피스 순위</h2>
    <div class="movie-list">
      <MovieCard v-for="(movie, index) in populaMovies" :key="movie.id" :movie="movie" type="popular" :index="index" />
    </div>

    <h2>현재 상영작</h2>
    <div class="movie-list">
      <MovieCard v-for="movie in nowPlayingMovies" :key="movie.id" :movie="movie" type="nowplaying" />
    </div>

    <h2>개봉예정작</h2>
    <div class="movie-list">
      <MovieCard v-for="movie in upComingMovies" :key="movie.id" :movie="movie" type="upcoming" />
    </div>
  </div>
</template>

<script setup>
import MovieCard from "@/components/MovieCard.vue";
import axios from "axios";
import { onMounted, ref } from "vue";

const populaMovies = ref([]);
const nowPlayingMovies = ref([]);
const upComingMovies = ref([]);

const API_KEY =
  "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YjI0YzA4NjJkNTQwODFmYjE0Y2VhZGMwMWZkODI4MCIsIm5iZiI6MTczMTY0NzQ1Ni42NDg5MzUzLCJzdWIiOiI2NzM2ZDc0MWZmZTM4NzhlOWU5ZmFmYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.eYQu1H6KBYqKX0e-WvHcWIH3AT1ioH1j-4OmFLxxUxk";

// 박스오피스 순위
const getPopularMovies = () => {
  axios({
    method: "get",
    url: "https://api.themoviedb.org/3/movie/popular?language=ko-KR&region=KR&page=1",
    headers: {
      accept: "application/json",
      Authorization: API_KEY,
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
      Authorization: API_KEY,
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
      Authorization: API_KEY,
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
.movie-list {
  display: flex;
  gap: 20px;
  overflow-x: scroll;
}
</style>
