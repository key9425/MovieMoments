<template>
  <div class="movie-container">
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
              <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: movie.id } }">
                <div class="movie-image-container">
                  <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" :alt="movie.title" class="movie-image" />
                </div>

                <div class="movie-info">
                  <h3 class="movie-title">{{ movie.title }}</h3>
                  <div class="movie-meta">
                    <span>{{ movie.release_date.substring(0, 4) }}</span>
                    <span class="dot">·</span>
                    <!-- 장르 데이터 오게되면 수정 -->
                    <span>{{ movie.genre }}</span>
                  </div>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 검색창 -->
    <!-- 검색 기능 -->
    <div class="search-section">
      <div class="search-container">
        <input type="text" v-model="searchKeyword" @input="handleSearch" placeholder="영화 제목을 입력하세요." class="search-input" @focus="isSearchFocused = true" @blur="handleSearchBlur" />
      </div>

      <!-- 검색 결과 드롭다운 -->
      <div v-if="isSearchFocused && (searchResults.length > 0 || searchKeyword)" class="search-results-dropdown">
        <div v-if="searchResults.length > 0" class="search-results">
          <RouterLink v-for="movie in searchResults" :key="movie.id" :to="{ name: 'MovieDetailView', params: { movieId: movie.id } }" class="movie-item">
            <div class="movie-poster-wrapper">
              <img :src="movie.poster_path ? `https://image.tmdb.org/t/p/w92${movie.poster_path}` : '/no-poster.jpg'" :alt="movie.title" class="movie-poster" />
            </div>
            <div class="movie-item-info">
              <h3 class="movie-item-title">{{ movie.title }}</h3>
              <p class="movie-item-year">{{ new Date(movie.release_date).getFullYear() }}</p>
            </div>
          </RouterLink>
        </div>
        <div v-else class="no-results">"{{ searchKeyword }}" 에 대한 검색 결과가 없습니다.</div>
      </div>
    </div>
    <br />

    <h2>박스오피스 순위</h2>
    <div class="movie-list">
      <MovieCard v-for="(movie, index) in populaMovies" :key="movie.id" :movie="movie" type="popular" :index="index" />
    </div>
    <br />

    <h2>현재 상영작</h2>
    <div class="movie-list">
      <MovieCard v-for="movie in nowPlayingMovies" :key="movie.id" :movie="movie" type="nowplaying" />
    </div>
    <br />

    <h2>개봉예정작</h2>
    <div class="movie-list">
      <MovieCard v-for="movie in upComingMovies" :key="movie.id" :movie="movie" type="upcoming" />
    </div>
  </div>
  <br />
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

// 개봉예정작
const getupComingMovies = () => {
  axios({
    method: "get",
    url: "https://api.themoviedb.org/3/movie/upcoming?language=ko-KR&page=1",

    headers: {
      accept: "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
  })
    .then((response) => {
      console.log("response = ", response);
      upComingMovies.value = response.data.results;
    })
    .catch((error) => {
      console.log("error = ", error);
    });
};

onMounted(() => {
  getPopularMovies(), getnowPlayingMovies(), getupComingMovies();
});
</script>

<style scoped>
/* 영화 */

.movie-container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 20px;
}
.movie-list {
  display: flex;
  gap: 20px;
  overflow-x: scroll;
  padding: 20px 0;
}

/* 검색모달 */
.search-input {
  width: 100%;
  border: 1px solid #ddd;

  border-radius: 4px;
  position: center;
  text-align: left;
  display: block; /* 추가 */
  margin: 50px auto; /* 상하 여백 30px, 가운데 정렬 */
  margin-bottom: 20px;
  background-color: #f5f5f5;
  cursor: pointer; /* 마우스 오버시 포인터 변경 */
}

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

/* 검색을 위한 스타일 추가 */
.search-section {
  position: relative;
  /* max-width: 600px; */
  margin: 0 70px;
}

.search-container {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 15px 45px 15px 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
  border: none;
}

.search-input:hover {
  background-color: #ebebeb;
}

.search-input:focus {
  border-color: #666;
  box-shadow: 0 0 0 3px rgba(102, 102, 102, 0.1);
  outline: none;
}

.search-results-dropdown {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  right: 0;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
}

.search-results {
  padding: 10px 0;
}

.movie-item {
  display: flex;
  padding: 10px 20px;
  text-decoration: none;
  color: inherit;
  transition: background-color 0.2s ease;
}

.movie-item:hover {
  background-color: #f8f9fa;
}

.movie-poster-wrapper {
  width: 50px;
  height: 75px;
  margin-right: 15px;
  overflow: hidden;
  border-radius: 4px;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.movie-item-title {
  font-size: 16px;
  font-weight: 500;
  margin: 0;
  color: #333;
}

.movie-item-year {
  font-size: 14px;
  color: #666;
  margin: 4px 0 0 0;
}

.no-results {
  padding: 20px;
  text-align: center;
  color: #666;
}

/* 스크롤바 스타일링 */
.search-results-dropdown::-webkit-scrollbar {
  width: 8px;
}

.search-results-dropdown::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.search-results-dropdown::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.search-results-dropdown::-webkit-scrollbar-thumb:hover {
  background: #666;
}

a {
  text-decoration: none;
}
</style>
