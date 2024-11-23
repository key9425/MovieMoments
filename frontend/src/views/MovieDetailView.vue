<template>
  <div v-if="movie">
    <!-- 백드롭 이미지 섹션 (전체 폭) -->
    <div class="position-relative movie-backdrop mb-4">
      <img :src="`https://image.tmdb.org/t/p/original/${movie.backdrop_path}`" :alt="movie.title" class="w-100" />
      <!-- 영화 정보 오버레이 -->
      <div class="movie-info-overlay">
        <div class="container">
          <h1 class="display-4 text-white mb-2">{{ movie.title }}</h1>
          <div class="d-flex flex-wrap align-items-center text-white gap-3">
            <span>{{ new Date(movie.release_date).getFullYear() }}</span>
            <span>•</span>
            <span>{{ movie.runtime }}분</span>
            <span>•</span>
            <span>{{ movie.genres?.map((genre) => genre.name).join(", ") }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 컨테이너 내부 콘텐츠 -->
    <div class="container">
      <div class="row">
        <!-- 왼쪽 열 - 포스터 -->
        <div class="col-md-4 mb-4">
          <div class="text-center">
            <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" :alt="movie.title" class="img-fluid rounded mb-3" />
            <div class="d-grid gap-2">
              <!-- ============================================================================ -->
              <!-- 찜하기 버튼 -->
              <button v-if="!isLiked" @click="likeMovie" class="btn btn-outline-danger">
                <i class="fas fa-heart me-2"></i>
                찜하기
              </button>
              <button v-else @click="unlikeMovie" class="btn btn-danger">
                <i class="fas fa-heart me-2"></i>
                찜취소
              </button>
              <!-- ============================================================================ -->
            </div>
          </div>
        </div>

        <!-- 오른쪽 열 - 상세 정보 -->
        <div class="col-md-8">
          <!-- 통계 -->
          <div class="row mb-4">
            <div class="col-6 col-md-3 mb-3">
              <div class="d-flex align-items-center">
                <i class="fas fa-star text-warning me-2"></i>
                <span>{{ formatVoteAverage(movie.vote_average) }}</span>
              </div>
            </div>
            <div class="col-6 col-md-3 mb-3">
              <div class="d-flex align-items-center">
                <i class="fas fa-users text-primary me-2"></i>
                <span>{{ formatNumber(movie.vote_count) }}명 평가</span>
              </div>
            </div>
          </div>

          <!-- 개요 -->
          <div class="card mb-4">
            <div class="card-header">
              <h2 class="h5 mb-0">작품 정보</h2>
            </div>
            <div class="card-body">
              <p class="card-text">{{ movie.overview }}</p>
            </div>
          </div>

          <!-- 추가 통계 -->
          <div class="card">
            <div class="card-body">
              <div class="row">
                <div class="col-6 mb-3">
                  <p class="text-muted mb-1">제작비</p>
                  <p class="h6">
                    {{ movie.budget > 0 ? formatCurrency(movie.budget) : "정보 없음" }}
                  </p>
                </div>
                <div class="col-6 mb-3">
                  <p class="text-muted mb-1">수익</p>
                  <p class="h6">
                    {{ movie.revenue > 0 ? formatCurrency(movie.revenue) : "정보 없음" }}
                  </p>
                </div>
                <div class="col-6">
                  <p class="text-muted mb-1">상태</p>
                  <p class="h6">{{ movie.status === "Released" ? "개봉됨" : "미개봉" }}</p>
                </div>
                <div class="col-6">
                  <p class="text-muted mb-1">원어</p>
                  <p class="h6">{{ movie.original_language?.toUpperCase() }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="container mt-4 text-center">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const route = useRoute();
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
    url: `${store.API_URL}/api/v1/movies/${props.movieId}/like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
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
    url: `${store.API_URL}/api/v1/movies/${props.movieId}/like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      isLiked.value = true;
    })
    .catch((error) => {
      console.error("찜하기 실패:", error);
    });
};

// 찜취소
const unlikeMovie = () => {
  axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/movies/${props.movieId}/like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      isLiked.value = false;
    })
    .catch((error) => {
      console.error("찜취소 실패:", error);
    });
};

// 컴포넌트 마운트 시 찜 상태 확인
onMounted(() => {
  checkLikeStatus();
});
// ======================================================

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
});
</script>

<style scoped>
.movie-backdrop {
  height: 600px;
  overflow: hidden;
  position: relative;
}

.movie-backdrop img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.2));
}

.movie-info-overlay {
  position: absolute;
  bottom: 2rem;
  left: 0;
  right: 0;
  padding: 1rem;
}

.gap-3 {
  gap: 1rem;
}

/* 이미지 로딩 중 스켈레톤 효과 */
img {
  min-height: 200px;
  background-color: #e9ecef;
}
/* 버튼에 호버 효과 추가 */
.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}
</style>
