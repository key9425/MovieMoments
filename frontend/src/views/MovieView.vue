<template>
  <div class="movie-container">
    <!-- 히어로 섹션 -->
    <section class="hero-section">
      <div class="hero-content container">
        <h1 class="main-title">영화 검색</h1>
        <!-- 검색창 -->
        <div class="search-wrapper">
          <input type="text" v-model="searchKeyword" @input="handleSearch" placeholder="영화 제목을 입력해주세요." class="search-input" @focus="isSearchFocused = true" @blur="handleSearchBlur" />
          <!-- 검색 결과 드롭다운 -->
          <div v-if="isSearchFocused && (searchResults.length > 0 || searchKeyword)" class="search-results-dropdown">
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
    </section>

    <!-- 추천 영화 섹션 -->
    <section class="movie-section container">
      <h2 class="section-title">추천 영화</h2>
      <div class="content-wrapper">
        <div v-if="loadingMovies" class="loading-state">
          <div class="spinner"></div>
          <p>영화를 불러오는 중...</p>
        </div>
        <div v-else-if="movieError" class="error-state">
          {{ movieError }}
        </div>
        <div v-else class="movie-grid">
          <RouterLink v-for="movie in recommendedMovies" :key="movie.id" :to="{ name: 'MovieDetailView', params: { movieId: movie.id } }" class="movie-card">
            <div class="poster-wrapper">
              <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" :alt="movie.title" class="movie-poster" />
              <div class="movie-overlay">
                <div class="movie-rating">
                  <i class="fas fa-star"></i>
                  {{ (movie.vote_average || 0).toFixed(1) }}
                </div>
              </div>
            </div>
            <div class="movie-info">
              <h3>{{ movie.title }}</h3>
              <div class="movie-meta">
                <span>{{ movie.release_date?.substring(0, 4) }}</span>
                <span class="separator">•</span>
                <span>{{ movie.genre }}</span>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- 박스오피스 섹션 -->
    <section class="movie-section container">
      <h2 class="section-title">박스오피스</h2>
      <div class="content-wrapper">
        <div class="movie-scroll">
          <MovieCard v-for="(movie, index) in populaMovies" :key="movie.id" :movie="movie" :index="index" type="popular" />
        </div>
      </div>
    </section>

    <!-- 현재 상영작 섹션 -->
    <section class="movie-section container">
      <h2 class="section-title">현재 상영작</h2>
      <div class="content-wrapper">
        <div class="movie-scroll">
          <MovieCard v-for="movie in nowPlayingMovies" :key="movie.id" :movie="movie" type="nowplaying" />
        </div>
      </div>
    </section>

    <!-- 개봉 예정작 섹션 -->
    <section class="movie-section container">
      <h2 class="section-title">개봉 예정작</h2>
      <div class="content-wrapper">
        <div class="movie-scroll">
          <MovieCard v-for="movie in upComingMovies" :key="movie.id" :movie="movie" type="upcoming" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import MovieCard from "@/components/MovieCard.vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { onMounted, ref } from "vue";
import { debounce } from "lodash";

const populaMovies = ref([]);
const nowPlayingMovies = ref([]);
const upComingMovies = ref([]);
const recommendedMovies = ref([]);
const loadingMovies = ref(true);
const movieError = ref(null);

const store = useCounterStore();
const API_KEY = import.meta.env.VITE_TMDB_API_KEY;
const API_URL = store.API_URL;

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

const searchKeyword = ref("");
const searchResults = ref([]);

// 영화 검색 관련
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
      console.log(searchResults.value);
    })
    .catch((error) => {
      console.error("영화 검색 에러:", error);
    });
};

// 검색 관련 상태 추가
const isSearchFocused = ref(false);

// 검색 blur 핸들러 추가
const handleSearchBlur = () => {
  // 약간의 지연을 줘서 링크 클릭이 가능하도록 함
  setTimeout(() => {
    isSearchFocused.value = false;
  }, 200);
};

const handleSearch = debounce((event) => {
  searchMovies(searchKeyword.value);
});

// 박스오피스 순위
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
      console.log("response = ", response);
      populaMovies.value = response.data.results;
    })
    .catch((error) => {
      console.log("error = ", error);
    });
};

// 현재상영작
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
      console.log("response = ", response);
      nowPlayingMovies.value = response.data.results;
    })
    .catch((error) => {
      console.log("error = ", error);
    });
};

// 개봉예정작 함수 수정
const getupComingMovies = async () => {
  try {
    // 여러 페이지의 결과를 가져오기
    const totalPages = 5; // 예시로 5페이지
    let allMovies = [];

    for (let page = 1; page <= totalPages; page++) {
      const response = await axios({
        method: "get",
        url: `https://api.themoviedb.org/3/movie/upcoming`,
        params: {
          language: "ko-KR",
          region: "KR", // 한국 지역 추가
          page: page,
        },
        headers: {
          accept: "application/json",
          Authorization: `Bearer ${API_KEY}`,
        },
      });

      allMovies = [...allMovies, ...response.data.results];
    }

    // 현재 날짜 이후의 영화만 필터링
    const today = new Date();
    const filteredMovies = allMovies.filter((movie) => {
      const releaseDate = new Date(movie.release_date);
      return releaseDate > today;
    });

    // 개봉일 기준으로 정렬
    upComingMovies.value = filteredMovies.sort((a, b) => {
      return new Date(a.release_date) - new Date(b.release_date);
    });

    console.log("Upcoming movies:", upComingMovies.value);
  } catch (error) {
    console.log("error = ", error);
  }
};

onMounted(() => {
  getPopularMovies(), getnowPlayingMovies(), getupComingMovies();
});
</script>

<style scoped>
.movie-container {
  background-color: #f8f9fa;
  min-height: 100vh;
}

/* 히어로 섹션 */
.hero-section {
  background: linear-gradient(to bottom, #1a1a1a, #2c2c2c);
  padding: 4rem 0;
  margin-bottom: 2rem;
}

.hero-content {
  text-align: center;
}

.main-title {
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* 검색 관련 스타일 */
.search-wrapper {
  max-width: 600px;
  margin: 0 auto;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  border: none;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.search-input:focus {
  background-color: rgba(255, 255, 255, 0.15);
  outline: none;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
}

.search-results-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
  background: white;
  border-radius: 12px;
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
}

/* 섹션 공통 스타일 */
.container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 1rem;
}

.movie-section {
  margin-bottom: 3rem;
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

/* 영화 그리드 */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  padding: 0.5rem;
}

/* 영화 스크롤 */
.movie-scroll {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 0.5rem;
  scroll-padding: 1rem;
  scroll-snap-type: x mandatory;
}

.movie-scroll::-webkit-scrollbar {
  height: 8px;
}

.movie-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.movie-scroll::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

/* 영화 카드 */
.movie-card {
  text-decoration: none;
  color: inherit;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  scroll-snap-align: start;
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

.separator {
  margin: 0 0.5rem;
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

@media (max-width: 768px) {
  .hero-section {
    padding: 2rem 0;
  }

  .main-title {
    font-size: 2rem;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }

  .movie-info h3 {
    font-size: 0.9rem;
  }

  .movie-meta {
    font-size: 0.8rem;
  }

  /* MovieView의 style 태그 내에 추가 */

  /* 추천 영화 섹션 스타일 */
  .movie-section:nth-child(2) {
    background-color: #1a1a1a;
    padding: 3rem 0;
    margin: -2rem 0 3rem 0;
  }

  .movie-section:nth-child(2) .section-title {
    color: white;
  }

  .movie-section:nth-child(2) .section-title::after {
    background: #ffd700;
  }

  /* 박스오피스 섹션 스타일 */
  .movie-section:nth-child(3) {
    background-color: #f8f9fa;
    padding: 3rem 0;
  }

  .movie-section:nth-child(3) .section-title::after {
    background: #dc3545;
  }

  /* 현재 상영작 섹션 스타일 */
  .movie-section:nth-child(4) {
    background-color: white;
    padding: 3rem 0;
  }

  .movie-section:nth-child(4) .section-title::after {
    background: #0d6efd;
  }

  /* 개봉 예정작 섹션 스타일 */
  .movie-section:nth-child(5) {
    background-color: #f8f9fa;
    padding: 3rem 0;
  }

  .movie-section:nth-child(5) .section-title::after {
    background: #198754;
  }
}
</style>
