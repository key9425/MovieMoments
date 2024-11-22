<template>
  <div>
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
                  <!-- 장르 데이터 오게되면 수정 -->
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

    <!-- 검색창 -->
    <!-- 검색창을 눌렀을 때 모달창을 띄우는게 필요하니까 버튼임 -->
    <div class="search-container">
      <input type="text" placeholder="영화검색" class="search-btn" />
      <button type="button" @click="openModal" class="search-btn">영화 제목을 입력해주세요.</button>
    </div>
    <SearchModal :is-open="isModalOpen" @close="closeModal" />
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
import SearchModal from "@/components/SearchModal.vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { onMounted, ref } from "vue";

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

// 모달
const isModalOpen = ref(false);

const openModal = () => {
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

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
.movie-list {
  display: flex;
  gap: 20px;
  overflow-x: scroll;
  padding: 20px 0;
}

/* 검색모달 */
.search-btn {
  width: 1000px;
  height: 50px;
  border-style: none;
  position: center;
  border-radius: 10px;
  text-align: left;
  display: block; /* 추가 */
  margin: 50px auto; /* 상하 여백 30px, 가운데 정렬 */
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
</style>
