<template>
  <div style="width: 18rem">
    <div v-if="movie">
      <h1>MovieDetailView</h1>

      <br />
      <h2>****영화 예고편 받아와서 띄우기 ****</h2>
      <br />
      <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" class="card-img-top" alt="..." />
      <p>{{ movie.title }}</p>
      <p>{{ movie.overview }}</p>
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

<style scoped></style>
