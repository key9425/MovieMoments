<template>
<!-- 상단 제목 -->
<section>
  <div class="header-section">
    <h2 class="main-title">오늘의 추천 영화</h2>
  </div>
</section>

<!-- 추천영화 섹션 -->
<section>
  <div class="recommended-movies">
    <div v-if="loadingMovies" class="text-center py-4">로딩 중...</div>
    <div v-else-if="movieError" class="text-red-500 py-4">
      {{ movieError }}
    </div>
    <div v-else class="movies-scroll">
      <div class="movies-row">
        <div v-for="movie in recommendedMovies" :key="movie.id" class="movie-card">
          <div class="movie-image-container">
            <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" :alt="movie.title" class="movie-image" />
          </div>
          <div class="movie-info">
            <h3 class="movie-title">{{ movie.title }}</h3>
            <div class="movie-meta">
              <span>{{ movie.release_date.substring(0, 4) }}</span>
              <span class="dot">·</span>
              <span>{{ movie.country || "미국" }}</span>
              <span class="dot">·</span>
              <span>{{ movie.genre || "드라마" }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
</template>

<script setup>
// 상태 관리
const recommendedMovies = ref([]);
const loadingMovies = ref(true);
const movieError = ref(null);

// 추천 영화 데이터 가져오기
const fetchRecommendedMovies = () => {
  loadingMovies.value = true;
  movieError.value = null;

  axios({
    method: "get",
    url: `${API_URL}/api/v1/recommended-movies/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("추천영화:", response);
      recommendedMovies.value = response.data.recommended_movies;
    })
    .catch((error) => {
      movieError.value = "영화 정보를 불러오는데 실패했습니다.";
      console.error("Error fetching recommended movies:", error);
    })
    .finally(() => {
      loadingMovies.value = false;
    });
};

onMounted(() => {
  fetchRecommendedMovies();
});
</script>

<style  scoped>
/* 추천 영화 섹션 */
.recommended-movies {
  margin: 2rem 0;
}

.movies-scroll {
  overflow-x: auto;
  padding: 1rem 0;
}

/* 스크롤바 스타일링 */
.movies-scroll::-webkit-scrollbar {
  height: 8px;
}

.movies-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.movies-scroll::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.movies-scroll::-webkit-scrollbar-thumb:hover {
  background: #666;
}

.movies-row {
  display: flex;
  gap: 1.5rem;
  padding: 0.5rem 0 1.5rem 0;
}

.movie-card {
  flex: 0 0 auto;
  width: 200px;
}

.movie-image-container {
  position: relative;
  height: 280px;
  border-radius: 4px;
  overflow: hidden;
}

.movie-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.2s ease;
}

.movie-card:hover .movie-image {
  transform: scale(1.05);
}

.movie-info {
  padding: 0.8rem 0;
}

.movie-title {
  font-size: 1rem;
  font-weight: 600;
  color: #3a3a3a;
  margin-bottom: 0.4rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.movie-meta {
  font-size: 0.9rem;
  color: #666;
}

.dot {
  margin: 0 0.3rem;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .movie-card {
    width: 150px;
  }

  .movie-image-container {
    height: 210px;
  }
}
</style>