<!-- SearchModal.vue -->
<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-content">
      <!-- 모달 제목 -->
      <div class="modal-header">
        <h2>영화 검색</h2>
        <button @click="closeModal" class="close-button">&times;</button>
      </div>
      <!-- 모달 내용 -->
      <!-- - 검색 기능 + 검색 결과가 여기에 들어오게 됨 -->
      <!-- 검색 기능 -->
      <div class="search-container">
        <input type="text" v-model="searchKeyword" @input="handleSearch" placeholder="영화 제목을 입력하세요." class="search-input" />
      </div>
      <!-- 검색 결과 -->
      <div class="search-results" v-if="searchResults.length">
        <div v-for="movie in searchResults" :key="movie.id" class="movie-item">
          <!-- 검색한 거 누르면 detail 패이지로 이동 -->
          <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: movie.id } }">
            <img :src="movie.poster_path ? `https://image.tmdb.org/t/p/w92${movie.poster_path}` : '/no-poster.jpg'" :alt="movie.title" class="movie-poster" />
            <div class="movie-info">
              <h3>{{ movie.title }}</h3>
              <p>{{ new Date(movie.release_date).getFullYear() }}</p>
            </div>
          </RouterLink>
        </div>
      </div>
      <div v-else-if="searchKeyword && !searchResults.length" class="no-results">검색 결과가 없습니다.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import { debounce } from "lodash";

const API_KEY =
  "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YjI0YzA4NjJkNTQwODFmYjE0Y2VhZGMwMWZkODI4MCIsIm5iZiI6MTczMTY0NzQ1Ni42NDg5MzUzLCJzdWIiOiI2NzM2ZDc0MWZmZTM4NzhlOWU5ZmFmYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.eYQu1H6KBYqKX0e-WvHcWIH3AT1ioH1j-4OmFLxxUxk";

const props = defineProps({
  isOpen: Boolean,
  apiKey: String,
});

const emit = defineEmits(["close"]);

const searchKeyword = ref("");
const searchResults = ref([]);

const closeModal = () => {
  emit("close");
  searchKeyword.value = "";
  searchResults.value = [];
};

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
      Authorization: API_KEY,
    },
  })
    .then((response) => {
      searchResults.value = response.data.results;
    })
    .catch((error) => {
      console.error("영화 검색 에러:", error);
    });
};

const handleSearch = debounce((event) => {
  searchMovies(searchKeyword.value);
});
</script>

<style scoped>
a {
  color: black;
  text-decoration: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 20px;
}

.movie-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.movie-item a {
  display: flex;
  gap: 15px;
  align-items: center; /* 세로 중앙 정렬 추가 */
  text-decoration: none;
  color: inherit;
}

.movie-info {
  flex: 1;
}

.movie-info h3 {
  margin: 0 0 8px 0;
}

.movie-info p {
  color: #666;
  margin: 0;
}

.no-results {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>
