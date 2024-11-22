<template>
  <RouterLink :to="{ name: 'GroupWatchedMovie', params: { group_id: groupId, group_movie_id: watchedMovie.id } }" class="card-link">
    <div class="polaroid-card">
      <!-- 영화 포스터 -->
      <div class="poster-container">
        <img :src="`https://image.tmdb.org/t/p/w500${watchedMovie.movie.poster_path}`" :alt="watchedMovie.movie.title" class="movie-poster" />
        <div class="poster-overlay">
          <span class="view-details">자세히 보기</span>
        </div>
      </div>

      <!-- 영화 정보 -->
      <div class="movie-info">
        <h3 class="movie-title">{{ watchedMovie.movie.title }}</h3>
        <p class="watch-date">{{ formatDate(watchedMovie.watched_date) }}</p>
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

const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};
</script>

<style scoped>
.card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.polaroid-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.polaroid-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.poster-container {
  position: relative;
  aspect-ratio: 2/3;
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.polaroid-card:hover .movie-poster {
  transform: scale(1.05);
}

.poster-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.polaroid-card:hover .poster-overlay {
  opacity: 1;
}

.view-details {
  color: white;
  background: rgba(0, 0, 0, 0.6);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.movie-info {
  padding: 1rem;
  text-align: center;
}

.movie-title {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.watch-date {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

/* 스켈레톤 로딩 효과 */
.movie-poster {
  background-color: #f0f0f0;
  min-height: 100%;
}
</style>
