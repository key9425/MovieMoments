<template>
  <div class="movie-container">
    <br />
    <!-- 추천영화 섹션 -->
    <section class="movie-section">
      <div class="content-wrapper">
        <h2 class="section-title">오늘의 추천 영화</h2>
        <div v-if="loadingMovies" class="loading-state">
          <div class="spinner"></div>
          <p>로딩 중...</p>
        </div>
        <div v-else-if="movieError" class="error-state">
          {{ movieError }}
        </div>
        <div v-else class="carousel-container" :style="{ width: `${carouselConfig.totalWidth}px`, margin: '0 auto' }">
          <button v-if="canSlidePrev.recommend" class="carousel-button prev" @click="slide('recommend', 'prev')">
            <i class="fas fa-chevron-left"></i>
          </button>
          <div class="carousel-wrapper" :style="{ width: `${carouselConfig.totalWidth}px` }">
            <div
              class="movie-carousel"
              :style="{
                transform: `translateX(-${currentSlide.recommend * (CARD_WIDTH + CARD_GAP)}px)`,
                gap: `${CARD_GAP}px`,
              }"
            >
              <RouterLink v-for="movie in recommendedMovies" :key="movie.id" :to="{ name: 'MovieDetailView', params: { movieId: movie.id } }" class="movie-card" :style="{ width: `${CARD_WIDTH}px` }">
                <div class="poster-wrapper">
                  <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" :alt="movie.title" class="movie-poster" />
                  <div class="movie-overlay">
                    <div class="movie-info">
                      <h3>{{ movie.title }}</h3>
                      <div class="movie-meta">
                        <span>{{ movie.release_date?.substring(0, 4) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </RouterLink>
            </div>
          </div>
          <button v-if="canSlideNext.recommend" class="carousel-button next" @click="slide('recommend', 'next')">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- 검색창 영역 -->
    <div class="search-section">
      <!-- 검색창 -->
      <div class="search-container">
        <i class="fas fa-search search-icon"></i>
        <input type="text" v-model="searchKeyword" @input="handleSearch" placeholder="영화 제목을 입력해주세요." class="search-btn" @focus="isSearchFocused = true" @blur="handleSearchBlur" />
        <!-- 검색 결과 드롭다운 -->
        <div v-if="isSearchFocused && (searchResults.length > 0 || searchKeyword)" class="search-results-dropdown">
          <!-- <div v-if="searchResults.length > 0 || searchKeyword" class="search-results-dropdown"> -->
          <div v-if="searchResults.length > 0" class="search-results">
            <RouterLink v-for="movie in searchResults" :key="movie.id" :to="{ name: 'MovieDetailView', params: { movieId: movie.id } }" class="search-movie-item">
              <div class="search-movie-poster">
                <img :src="movie.poster_path ? `https://image.tmdb.org/t/p/w92${movie.poster_path}` : '/no-poster.jpg'" :alt="movie.title" />
              </div>
              <div class="search-movie-info">
                <h3>{{ movie.title }}</h3>
                <p>{{ new Date(movie.release_date).getFullYear() }}</p>
              </div>
            </RouterLink>
          </div>
          <div v-else class="no-results">"{{ searchKeyword }}" 에 대한 검색 결과가 없습니다.</div>
        </div>
      </div>
    </div>

    <!-- 박스오피스 섹션 -->
    <section class="movie-section" v-if="carouselConfig != null">
      <div class="content-wrapper">
        <h2 class="section-title">박스오피스</h2>
        <div class="carousel-container" :style="{ width: `${carouselConfig.totalWidth}px`, margin: '0 auto' }">
          <button v-if="canSlidePrev.popular" class="carousel-button prev" @click="slide('popular', 'prev')">
            <i class="fas fa-chevron-left"></i>
          </button>
          <div class="carousel-wrapper" :style="{ width: `${carouselConfig.totalWidth}px` }">
            <div
              class="movie-carousel"
              :style="{
                transform: `translateX(-${currentSlide.popular * (CARD_WIDTH + CARD_GAP)}px)`,
                gap: `${CARD_GAP}px`,
              }"
            >
              <MovieCard v-for="(movie, index) in populaMovies" :key="movie.id" :movie="movie" :index="index" :style="{ width: `${CARD_WIDTH}px` }" type="popular" />
            </div>
          </div>
          <button v-if="canSlideNext.popular" class="carousel-button next" @click="slide('popular', 'next')">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- 현재 상영작 섹션 -->
    <section class="movie-section" v-if="carouselConfig != null">
      <div class="content-wrapper">
        <h2 class="section-title">현재 상영작</h2>
        <div class="carousel-container" :style="{ width: `${carouselConfig.totalWidth}px`, margin: '0 auto' }">
          <button v-if="canSlidePrev.nowPlaying" class="carousel-button prev" @click="slide('nowPlaying', 'prev')">
            <i class="fas fa-chevron-left"></i>
          </button>
          <div class="carousel-wrapper" :style="{ width: `${carouselConfig.totalWidth}px`, margin: '0 auto' }">
            <div
              class="movie-carousel"
              :style="{
                transform: `translateX(-${currentSlide.nowPlaying * (CARD_WIDTH + CARD_GAP)}px)`,
                gap: `${CARD_GAP}px`,
              }"
            >
              <MovieCard v-for="movie in nowPlayingMovies" :key="movie.id" :movie="movie" :style="{ width: `${CARD_WIDTH}px` }" type="nowplaying" />
            </div>
          </div>
          <button v-if="canSlideNext.nowPlaying" class="carousel-button next" @click="slide('nowPlaying', 'next')">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- 개봉 예정작 섹션 -->
    <section class="movie-section" v-if="carouselConfig != null">
      <div class="content-wrapper">
        <h2 class="section-title">개봉 예정작</h2>
        <div class="carousel-container" :style="{ width: `${carouselConfig.totalWidth}px`, margin: '0 auto' }">
          <button v-if="canSlidePrev.upcoming" class="carousel-button prev" @click="slide('upcoming', 'prev')">
            <i class="fas fa-chevron-left"></i>
          </button>
          <div class="carousel-wrapper" :style="{ width: `${carouselConfig.totalWidth}px`, margin: '0 auto' }">
            <div
              class="movie-carousel"
              :style="{
                transform: `translateX(-${currentSlide.upcoming * (CARD_WIDTH + CARD_GAP)}px)`,
                gap: `${CARD_GAP}px`,
              }"
            >
              <MovieCard v-for="movie in upComingMovies" :key="movie.id" :movie="movie" :style="{ width: `${CARD_WIDTH}px` }" type="upcoming" />
            </div>
          </div>
          <button v-if="canSlideNext.upcoming" class="carousel-button next" @click="slide('upcoming', 'next')">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import MovieCard from "@/components/MovieCard.vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { debounce } from "lodash";
import { ref, onMounted, computed, onBeforeUnmount } from "vue";

const store = useCounterStore();
const API_KEY = import.meta.env.VITE_TMDB_API_KEY;
const API_URL = store.API_URL;

// 영화 데이터 상태
const populaMovies = ref([]);
const nowPlayingMovies = ref([]);
const upComingMovies = ref([]);
const recommendedMovies = ref([]);
const loadingMovies = ref(true);
const movieError = ref(null);
const carouselConfig = ref(null);

// 케러셀 관련 상수
const CARD_WIDTH = 224; // 카드 기본 너비
const CARD_GAP = 20; // 카드 간격
const CONTAINER_PADDING = 32; // 컨테이너 좌우 패딩

// 케러셀 상태
const currentSlide = ref({
  recommend: 0,
  popular: 0,
  nowPlaying: 0,
  upcoming: 0,
});

// 화면 크기에 따른 카드 수와 너비 계산
const calculateArea = () => {
  const containerWidth = Math.min(window.innerWidth - CONTAINER_PADDING, 1300);

  // 표시 가능한 최대 카드 수 계산
  const possibleCards = Math.floor(containerWidth / (CARD_WIDTH + CARD_GAP));

  // 실제 케러셀 너비 계산
  const carouselWidth = possibleCards * CARD_WIDTH + (possibleCards - 1) * CARD_GAP;

  console.log("넓이 정보", containerWidth, possibleCards, carouselWidth);

  return {
    cardsPerView: possibleCards,
    cardWidth: CARD_WIDTH, // 고정된 카드 너비 사용
    totalWidth: carouselWidth, // 케러셀에 필요한 정확한 너비
  };
};

// carouselConfig = computed(calculateArea);

// 각 섹션의 총 슬라이드 수 계산
const totalSlides = computed(() => ({
  recommend: Math.max(0, recommendedMovies.value.length - carouselConfig.value.cardsPerView),
  popular: Math.max(0, populaMovies.value.length - carouselConfig.value.cardsPerView),
  nowPlaying: Math.max(0, nowPlayingMovies.value.length - carouselConfig.value.cardsPerView),
  upcoming: Math.max(0, upComingMovies.value.length - carouselConfig.value.cardsPerView),
}));

// 슬라이드 이동 가능 여부
const canSlidePrev = computed(() => ({
  recommend: currentSlide.value.recommend > 0,
  popular: currentSlide.value.popular > 0,
  nowPlaying: currentSlide.value.nowPlaying > 0,
  upcoming: currentSlide.value.upcoming > 0,
}));

const canSlideNext = computed(() => ({
  recommend: currentSlide.value.recommend < totalSlides.value.recommend,
  popular: currentSlide.value.popular < totalSlides.value.popular,
  nowPlaying: currentSlide.value.nowPlaying < totalSlides.value.nowPlaying,
  upcoming: currentSlide.value.upcoming < totalSlides.value.upcoming,
}));

// 슬라이드 이동 함수
const slide = (type, direction) => {
  if (direction === "next" && canSlideNext.value[type]) {
    currentSlide.value[type]++;
  } else if (direction === "prev" && canSlidePrev.value[type]) {
    currentSlide.value[type]--;
  }
};

// 화면 크기 변경 감지
const handleResize = debounce(() => {
  carouselConfig.value = calculateArea();
}, 200);

// 검색 관련 상태와 함수
const searchKeyword = ref("");
const searchResults = ref([]);
const isSearchFocused = ref(false);

const searchMovies = (word) => {
  if (!word.trim()) {
    searchResults.value = [];
    return;
  }
  axios({
    method: "get",
    url: `https://api.themoviedb.org/3/search/movie?query=${encodeURIComponent(word)}&language=ko-KR&page=1`,
    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      searchResults.value = response.data.results;
    })
    .catch((error) => {
      console.error("영화 검색 에러:", error);
    });
};

const handleSearchBlur = () => {
  setTimeout(() => {
    isSearchFocused.value = false;
  }, 200);
};

const handleSearch = debounce((event) => {
  searchMovies(searchKeyword.value);
}, 300);

// 영화 데이터 가져오기 함수들
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

const getPopularMovies = () => {
  axios({
    method: "get",
    url: "https://api.themoviedb.org/3/movie/popular?language=ko-KR&region=KR&page=1",
    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      populaMovies.value = response.data.results;
    })
    .catch((error) => {
      console.error("Error fetching popular movies:", error);
    });
};

const getnowPlayingMovies = () => {
  axios({
    method: "get",
    url: "https://api.themoviedb.org/3/movie/now_playing?language=ko-KR&region=KR&page=1",
    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      nowPlayingMovies.value = response.data.results;
    })
    .catch((error) => {
      console.error("Error fetching now playing movies:", error);
    });
};

const getupComingMovies = async () => {
  try {
    const response = await axios({
      method: "get",
      url: "https://api.themoviedb.org/3/movie/upcoming",
      params: {
        language: "ko-KR",
        region: "KR",
        page: 1,
      },
      headers: {
        accept: "application/json",
        Authorization: `Bearer ${API_KEY}`,
      },
    });

    const today = new Date();
    const filteredMovies = response.data.results.filter((movie) => {
      const releaseDate = new Date(movie.release_date);
      return releaseDate > today;
    });

    upComingMovies.value = filteredMovies.sort((a, b) => {
      return new Date(a.release_date) - new Date(b.release_date);
    });
  } catch (error) {
    console.error("Error fetching upcoming movies:", error);
  }
};

// 컴포넌트 마운트 시 실행
onMounted(() => {
  window.addEventListener("resize", handleResize);

  fetchRecommendedMovies();
  getPopularMovies();
  getnowPlayingMovies();
  getupComingMovies();
  carouselConfig.value = calculateArea();
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
});
</script>

<style scoped>
.movie-container {
  background-color: #f8f9fa;
  min-height: 100vh;
}

/* 히어로 섹션 */
.hero-section {
  background-color: #1a1a1a;
  padding: 4rem 0;
}

.hero-content {
  text-align: center;
}

/* 검색 관련 스타일 */
/* 검색 섹션 */
.search-section {
  max-width: 1200px;
  margin: 20px auto 0;
  padding: 20px;
}

.search-container {
  position: relative; /* 추가 */
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #74747b;
  font-size: 0.9rem;
  z-index: 1; /* 추가 */
}

.search-btn {
  flex: 1;
  height: 50px;
  border: none;
  border-radius: 10px;
  text-align: left;
  padding-left: 36px; /* 20px에서 36px로 수정 - 아이콘 공간 확보 */
  background-color: #ebebeb;
}

.search-btn:hover {
  background-color: #d8d8d8;
}

.search-btn:focus {
  outline: none;
  background-color: #d8d8d8; /* 기존 스타일 대신 그룹 검색창과 동일하게 */
}

.search-input::placeholder {
  color: #666666; /* placeholder 색상을 더 진하게 수정 */
}

/* 검색 결과 드롭다운 스타일 유지 */
.search-results-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
  background: white;
  border-radius: 10px; /* 검색창과 동일한 radius */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  max-height: 400px;
  overflow-y: auto;
}

.search-movie-item {
  display: flex;
  padding: 1rem;
  text-decoration: none;
  color: inherit;
  transition: background-color 0.2s;
}

.search-movie-item:hover {
  background-color: #f8f9fa;
}

.search-movie-poster {
  width: 60px;
  height: 90px;
  border-radius: 6px;
  overflow: hidden;
  margin-right: 1rem;
}

.search-movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.search-movie-info h3 {
  margin: 0;
  font-size: 1rem;
  color: #1a1a1a;
}

.search-movie-info p {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: #6c757d;
  text-align: left;
}

.no-results {
  padding: 1rem;
}
/* 섹션 공통 스타일 */
.content-wrapper {
  max-width: 1300px;
  margin: 0 auto;
}

.movie-section {
  position: relative;
  padding-top: 4rem;
}
.movie-section:nth-last-child(1) {
  padding-bottom: 4rem;
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

/* 영화 그리드 스타일 */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.5rem;
  padding: 0.5rem;
  margin: 0 auto;
}

/* 케러셀 스타일 */
.carousel-container {
  position: relative;
  padding: 0.5rem 0;
}

.carousel-wrapper {
  overflow: hidden;
}

.movie-carousel {
  display: flex;
  transition: transform 0.3s ease;
}

/* 영화 카드 스타일 */
.movie-card {
  flex-shrink: 0;
  position: relative;
  text-decoration: none;
  color: inherit;
  background: white;
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.movie-card:hover {
  transform: translateY(-5px);
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

/* 캐러셀 네비게이션 버튼 */
.carousel-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(220, 53, 69, 0.9);
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.carousel-button:hover {
  background: #dc3545;
  transform: translateY(-50%) scale(1.1);
}

.carousel-button.prev {
  left: 0;
  transform: translate(-50%, -50%);
}

.carousel-button.next {
  right: 0;
  transform: translate(50%, -50%);
}

/* 로딩 상태 */
.loading-state {
  text-align: center;
  padding: 2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #dc3545;
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 에러 상태 */
.error-state {
  text-align: center;
  padding: 2rem;
  color: #dc3545;
}

/* 추천 영화 섹션 스타일 */
.movie-section:nth-child(2) {
  background-color: #1a1a1a;
  margin: -2rem 0 0 0;
  padding: 4rem 0;
}

.movie-section:nth-child(2) .section-title {
  color: white;
  font-size: 1.8rem;
}

.movie-section:nth-child(2) .section-title::after {
  background: #ffd700;
  width: 60px;
  height: 4px;
}

.movie-section:nth-child(2) .movie-card {
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transform-origin: center bottom;
  transition: all 0.3s ease;
}

.movie-section:nth-child(2) .movie-card:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.movie-section:nth-child(2) .poster-wrapper {
  position: relative;
  padding-top: 150%;
}

.movie-section:nth-child(2) .movie-poster {
  transition: transform 0.3s ease;
}

.movie-section:nth-child(2) .movie-card:hover .movie-poster {
  transform: scale(1.05);
}

.movie-section:nth-child(2) .movie-overlay {
  background: linear-gradient(to bottom, transparent 30%, rgba(0, 0, 0, 0.8) 100%);
}

.movie-section:nth-child(2) .movie-info {
  padding: 0;
}

.movie-section:nth-child(2) .movie-info h3 {
  color: #ffd700;
  font-size: 1.1rem;
  font-weight: 700;
  text-wrap: auto;
}

.movie-section:nth-child(2) .movie-meta {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  font-weight: 500;
}

/* 반응형 스타일 */
@media (max-width: 1200px) {
  .movie-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 992px) {
  .movie-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 2rem 0;
  }

  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .carousel-button {
    width: 36px;
    height: 36px;
    font-size: 1rem;
  }

  .movie-section:nth-child(2) {
    padding: 3rem 0;
  }

  .movie-section:nth-child(2) .section-title {
    font-size: 1.6rem;
  }

  .movie-section:nth-child(2) .movie-info h3 {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .main-title {
    font-size: 2rem;
  }

  .movie-info h3 {
    font-size: 0.9rem;
  }

  .movie-meta {
    font-size: 0.8rem;
  }

  .carousel-button {
    width: 32px;
    height: 32px;
  }
}
</style>
