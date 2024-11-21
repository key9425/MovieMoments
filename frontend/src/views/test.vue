<!-- MovieWatchCard.vue -->
<template>
  <RouterLink :to="{ name: 'GroupWatchedMovie', params: { group_id: groupId, movie_id: watchedMovie.id } }">
    <div class="movie-card">
      <div class="card" style="width: 18rem">
        <img :src="`https://image.tmdb.org/t/p/w200${watchedMovie.movie.poster_path}`" class="card-img-top" :alt="watchedMovie.movie.title" />
        <div class="card-body">
          <h5 class="card-title">{{ watchedMovie.movie.title }}</h5>
          <p class="card-text">{{ watchedMovie.watched_date }}</p>
        </div>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { RouterLink } from "vue-router";

const props = defineProps({
  watchedMovie: {
    type: Object,
    required: true,
  },
  groupId: {
    type: [String, Number],
    required: true,
  },
});
</script>
