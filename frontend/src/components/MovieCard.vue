<template>
  <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: movie.id } }" class="movie-card">
    <div class="poster-wrapper">
      <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" :alt="movie.title" class="movie-poster" />
      <div class="movie-overlay">
        <div class="movie-rating">
          <i class="fas fa-star"></i>
          {{ (movie.vote_average || 0).toFixed(1) }}
        </div>
      </div>

      <!-- 박스오피스 순위 표시 -->
      <div v-if="type === 'popular'" class="rank-badge">
        {{ index + 1 }}
      </div>

      <!-- 개봉예정작 D-day 표시 -->
      <div v-if="type === 'upcoming'" class="d-day-badge">D{{ calculateDday(movie.release_date) }}</div>
    </div>
    <div class="movie-info">
      <h3>{{ movie.title }}</h3>
      <div class="movie-meta">
        <span>{{ movie.release_date?.substring(0, 4) }}</span>
        <!-- 장르가 있을 경우에만 표시 -->
        <template v-if="mainGenre">
          <span class="separator">•</span>
          <span>{{ mainGenre }}</span>
        </template>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
  type: {
    type: String,
    required: true,
  },
  index: {
    type: Number,
    default: 0,
  },
});

// D-day 계산 함수
const calculateDday = (releaseDate) => {
  const today = new Date();
  const release = new Date(releaseDate);
  const diffTime = release - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays > 0 ? `-${diffDays}` : "+" + Math.abs(diffDays);
};

// 대표 장르 computed 속성
const mainGenre = computed(() => {
  const genreMap = {
    28: "액션",
    12: "모험",
    16: "애니메이션",
    35: "코미디",
    80: "범죄",
    99: "다큐멘터리",
    18: "드라마",
    10751: "가족",
    14: "판타지",
    36: "역사",
    27: "공포",
    10402: "음악",
    9648: "미스터리",
    10749: "로맨스",
    878: "SF",
    10770: "TV 영화",
    53: "스릴러",
    10752: "전쟁",
    37: "서부",
  };

  if (props.movie.genres?.length) {
    // 영화 상세 정보에서 오는 첫 번째 장르
    return props.movie.genres[0].name;
  } else if (props.movie.genre_ids?.length) {
    // 영화 목록에서 오는 첫 번째 장르
    return genreMap[props.movie.genre_ids[0]] || "";
  }
  return "";
});
</script>

<style scoped>
.movie-card {
  width: 200px;
  text-decoration: none;
  color: inherit;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  scroll-snap-align: start;
  flex-shrink: 0;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.poster-wrapper {
  position: relative;
  padding-top: 150%;
}

.movie-poster {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 50%, rgba(0, 0, 0, 0.7));
  opacity: 0;
  transition: opacity 0.2s;
  display: flex;
  align-items: flex-end;
  padding: 1rem;
}

.movie-card:hover .movie-overlay {
  opacity: 1;
}

/* 박스오피스 순위 배지 */
.rank-badge {
  position: absolute;
  bottom: 12px;
  left: 12px;
  color: white;
  font-size: 3.5rem;
  font-weight: 600;
  font-style: italic;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  z-index: 1;
  line-height: 1;
  font-family: "Arial", sans-serif;
}

/* D-day 배지 */
.d-day-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(0, 0, 0, 0.85);
  color: white;
  padding: 0.4rem 0.8rem;
  font-weight: 600;
  font-size: 0.9rem;
  border-radius: 6px;
  z-index: 1;
}

.movie-rating {
  color: white;
  font-weight: 600;
}

.movie-rating i {
  color: #ffd700;
  margin-right: 0.25rem;
}

.movie-info {
  padding: 1rem;
}

.movie-info h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.movie-meta {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #6c757d;
}

.separator {
  margin: 0 0.5rem;
}
</style>
