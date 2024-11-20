<template>
    <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: props.movie.id } }">
      <!-- 박스오피스 순위 -->
      <div v-if="props.type === 'popular'">
        <div class="card" style="width: 18rem">
          <img :src="`https://image.tmdb.org/t/p/w500/${props.movie.poster_path}`" class="card-img-top" alt="..." />
          <div class="card-body">
            <h5 class="card-title">제목 : {{ props.movie.title }}</h5>
            <p class="card-text">개봉일 : {{ props.movie.release_date }}</p>
            <p class="card-text" v-if="props.type === 'popular'">박스오피스 순위: {{ props.index + 1 }}위</p>
          </div>
        </div>
      </div>
  
      <!-- 현재상영작 -->
      <div v-else-if="props.type === 'nowplaying'">
        <div class="card" style="width: 18rem">
          <img :src="`https://image.tmdb.org/t/p/w500/${props.movie.poster_path}`" class="card-img-top" alt="..." />
          <div class="card-body">
            <h5 class="card-title">제목 : {{ props.movie.title }}</h5>
            <p class="card-text">개봉일 : {{ props.movie.release_date }}</p>
          </div>
        </div>
      </div>
  
      <!-- 개봉예정작 -->
      <div v-else-if="props.type === 'upcoming'">
        <div class="card" style="width: 18rem">
          <img :src="`https://image.tmdb.org/t/p/w500/${props.movie.poster_path}`" class="card-img-top" alt="..." />
          <div class="card-body">
            <h5 class="card-title">제목 : {{ props.movie.title }}</h5>
            <p class="card-text">개봉일 : {{ props.movie.release_date }}</p>
          </div>
        </div>
      </div>
    </RouterLink>
  </template>
  
  <script setup>
  import { RouterLink } from "vue-router";
  // props 여러개 정의
  const props = defineProps(["movie", "type", "index"]);
  </script>
  
  <style scoped>
  a {
    text-decoration: none;
  }
  </style>
  