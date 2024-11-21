<!-- MovieWatchCard.vue -->
<template>
  <RouterLink :to="{ name: 'GroupWatchedMovie', params: { group_id: groupId, group_movie_id: watchedMovie.id } }">
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
// props 여러개 정의
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

<style scoped>
a {
  text-decoration: none;
}
.movie-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.movie-info {
  padding: 1rem;
}

.movie-info h3 {
  margin: 0 0 0.5rem 0;
}

.movie-info p {
  margin: 0;
  color: #666;
}
</style>
