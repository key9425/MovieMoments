<template>
  <div v-if="movie" class="movie-detail">
    <!-- 백드롭 섹션 -->
    <div class="movie-hero position-relative">
      <img :src="`https://image.tmdb.org/t/p/original/${movie.backdrop_path}`" :alt="movie.title" class="hero-image" />
      <div class="hero-overlay"></div>
      <div class="hero-content container">
        <div class="row align-items-end">
          <div class="col-md-3">
            <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" :alt="movie.title" class="poster-image" />
          </div>
          <div class="col-md-9">
            <h1 class="movie-title text-white mb-3">{{ movie.title }}</h1>
            <div class="movie-meta text-white mb-4">
              <span>{{ new Date(movie.release_date).getFullYear() }}</span>
              <span class="mx-2">•</span>
              <span>{{ movie.runtime }}분</span>
              <span class="mx-2">•</span>
              <span>{{ movie.genres?.map((genre) => genre.name).join(", ") }}</span>
            </div>
            <!-- 평점과 찜하기 버튼 -->
            <div class="d-flex align-items-center gap-4">
              <div class="rating">
                <i class="fas fa-star text-warning me-2"></i>
                <span class="text-white">{{ formatVoteAverage(movie.vote_average) }}</span>
              </div>
              <button @click="likeMovie()" :class="['like-btn', isLiked ? 'liked' : '']">
                <i class="fas fa-heart"></i>
                찜하기
                <!-- {{ isLiked ? "보고싶어요" : "보고싶어요" }} -->
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="container py-5">
      <!-- 개요 섹션 -->
      <section class="movie-overview mb-5">
        <h2 class="section-title">작품 정보</h2>
        <p class="overview-text">{{ movie.overview }}</p>
        <div class="movie-stats mt-4">
          <div class="row g-4">
            <div class="col-6 col-md-3">
              <div class="stat-item">
                <h3 class="stat-label">제작비</h3>
                <p class="stat-value">{{ movie.budget > 0 ? formatCurrency(movie.budget) : "정보 없음" }}</p>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="stat-item">
                <h3 class="stat-label">수익</h3>
                <p class="stat-value">{{ movie.revenue > 0 ? formatCurrency(movie.revenue) : "정보 없음" }}</p>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="stat-item">
                <h3 class="stat-label">상태</h3>
                <p class="stat-value">{{ movie.status === "Released" ? "개봉됨" : "미개봉" }}</p>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="stat-item">
                <h3 class="stat-label">원어</h3>
                <p class="stat-value">{{ movie.original_language?.toUpperCase() }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 출연진 섹션 -->
      <section class="cast-section mb-5">
        <h2 class="section-title">출연진</h2>
        <div class="cast-scrollable">
          <div class="cast-list">
            <div v-for="cast in movieCasts.slice(0, 10)" :key="cast.id" class="cast-card">
              <div class="cast-image-wrapper">
                <img :src="cast.profile_path ? `https://image.tmdb.org/t/p/w185/${cast.profile_path}` : '/default-profile.png'" :alt="cast.name" class="cast-image" />
              </div>
              <div class="cast-info">
                <h3 class="cast-name">{{ cast.name }}</h3>
                <p class="cast-character">{{ cast.character }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 갤러리 섹션 -->
      <section class="gallery-section">
        <h2 class="section-title">갤러리</h2>
        <div class="row g-4">
          <div v-for="(image, index) in movieImages" :key="index" class="col-md-4">
            <div class="gallery-item">
              <img :src="`https://image.tmdb.org/t/p/w500/${image.file_path}`" :alt="`${movie.title} 이미지 ${index + 1}`" class="gallery-image" @click="openLightbox(image)" />
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const route = useRoute();
const movieImages = ref([]);
const movieCasts = ref([]);
const movie = ref(null);
const isLiked = ref(false);
const props = defineProps(["movie"]);
const store = useCounterStore();
const movieId = route.params.movieId;

const API_KEY = import.meta.env.VITE_TMDB_API_KEY;

// ======================================================
// 현재 영화가 찜한 상태인지 확인
const checkLikeStatus = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v2/like/`,
    params: { movie_id: movieId },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("response", response.data);
      isLiked.value = response.data.is_liked;
    })
    .catch((error) => {
      console.error("찜 상태 확인 실패:", error);
    });
};

// 찜하기
const likeMovie = () => {
  axios({
    method: "post",
    url: `${store.API_URL}/api/v2/like/`,
    data: {
      movie_id: movieId,
      title: movie.value.title,
      poster_path: movie.value.poster_path,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response.data);
      isLiked.value = response.data.is_liked;
    })
    .catch((error) => {
      console.error("찜하기 실패:", error);
    });
};

// 컴포넌트 마운트 시 찜 상태 확인
onMounted(() => {
  checkLikeStatus();
});

//  영화 상세정보 가져오기
const getMovieDetails = () => {
  axios({
    method: "get",
    url: `https://api.themoviedb.org/3/movie/${movieId}`,
    params: {
      language: "ko-KR",
    },
    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      movie.value = response.data;
    })
    .catch((error) => {
      console.error("Error fetching movie details:", error);
    });
};

// 영화 갤러리 정보 가져오기
const getMovieImages = () => {
  axios({
    method: "get",
    url: `https://api.themoviedb.org/3/movie/${movieId}/images`,
    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      // backdrop만 선택하고 랜덤으로 섞기
      const shuffledBackdrops = response.data.backdrops.sort(() => Math.random() - 0.5);

      // 앞에서 6개만 선택
      movieImages.value = shuffledBackdrops.slice(0, 6);

      console.log("랜덤 선택된 backdrop:", movieImages.value); // 디버깅용
    })
    .catch((error) => {
      console.error("Error fetching movie images:", error);
    });
};

// 영화 출연진(credits)
const getMovieCasts = () => {
  axios({
    method: "get",
    url: `https://api.themoviedb.org/3/movie/${movieId}/credits`,
    params: {
      language: "ko-KR",
    },
    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      movieCasts.value = response.data.cast;
      console.log(movieCasts.value);
    })
    .catch((error) => {
      console.error("Error fetching movie images:", error);
    });
};

const formatVoteAverage = (vote) => {
  return vote?.toFixed(1);
};

const formatNumber = (num) => {
  return num?.toLocaleString();
};

const formatCurrency = (amount) => {
  return `$${amount.toLocaleString()}`;
};

onMounted(() => {
  getMovieDetails();
  getMovieImages();
  getMovieCasts();
});
</script>

<style scoped>
.movie-detail {
  background-color: #f8f9fa;
}

.movie-hero {
  height: 600px;
  margin-bottom: 2rem;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.3));
}

.hero-content {
  position: absolute;
  bottom: 3rem;
  left: 0;
  right: 0;
}

.poster-image {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.movie-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.movie-meta {
  font-size: 1.1rem;
  opacity: 0.9;
}

.like-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: 2px solid #454545;
  background: transparent;
  color: white;
  font-weight: 600;
  transition: all 0.2s;
}

.like-btn.liked {
  background: #dc3545;
}

.like-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  position: relative;
}

.section-title::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -0.5rem;
  width: 50px;
  height: 3px;
  background: #dc3545;
}

/* 출연진 섹션 스타일 */
.cast-scrollable {
  overflow-x: auto;
  padding-bottom: 1rem;
}

.cast-list {
  display: flex;
  gap: 1.5rem;
  padding: 0.5rem;
}

.cast-card {
  flex: 0 0 160px;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.cast-card:hover {
  transform: translateY(-5px);
}

.cast-image-wrapper {
  width: 100%;
  padding-top: 150%;
  position: relative;
}

.cast-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cast-info {
  padding: 1rem;
}

.cast-name {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cast-character {
  font-size: 0.875rem;
  color: #6c757d;
  margin: 0.25rem 0 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 갤러리 섹션 스타일 */
.gallery-item {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.gallery-image {
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
  transition: transform 0.3s;
}

.gallery-image:hover {
  transform: scale(1.05);
}

/* 스타일 */
.stat-item {
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

@media (max-width: 768px) {
  .movie-hero {
    height: auto;
    padding-top: 2rem;
  }

  .hero-content {
    position: relative;
    bottom: 0;
    padding: 2rem 0;
  }

  .movie-title {
    font-size: 2rem;
  }

  .cast-card {
    flex: 0 0 140px;
  }
}
</style>
