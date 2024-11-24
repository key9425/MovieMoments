<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <h2>영화 추가하기</h2>
      <form @submit.prevent="handleSubmit">
        <!-- 영화 검색 -->
        <div class="form-group">
          <label>영화 검색</label>
          <input type="text" v-model="searchKeyword" @input="searchMovies" placeholder="영화 제목을 입력하세요" />
          <!-- 검색 결과 목록 -->
          <div v-if="searchResults.length > 0" class="search-results">
            <div v-for="movie in searchResults" :key="movie.id" @click="selectMovie(movie)" class="search-item">
              <img :src="`https://image.tmdb.org/t/p/w92${movie.poster_path}`" :alt="movie.title" />
              <div class="movie-details">
                <p class="movie-title">{{ movie.title }}</p>
                <p class="movie-year">
                  {{ movie.release_date?.split("-")[0] }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 선택된 영화 표시 -->
        <div v-if="selectedMovie" class="selected-movie">
          <img :src="`https://image.tmdb.org/t/p/w200${selectedMovie.poster_path}`" :alt="selectedMovie.title" />
          <h3>{{ selectedMovie.title }}</h3>
        </div>

        <!-- 관람일 선택 -->
        <div class="form-group">
          <label>관람일</label>
          <input type="date" v-model="watchedDate" required />
        </div>

        <div class="button-group">
          <button type="button" @click="$emit('close')" class="cancel-btn" :disabled="isSaving">취소</button>
          <button type="submit" class="submit-btn" :disabled="!selectedMovie || !watchedDate || isSaving">
            <span v-if="isSaving" class="spinner-border spinner-border-sm me-2" role="status"></span>
            {{ isSaving ? "저장중..." : "추가하기" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
// GroupMovieCreateModal.vue의 script 부분 수정
import { ref, watch } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from "vue-router";
import { debounce } from "lodash";

const store = useCounterStore();
const route = useRoute();
const router = useRouter();

const searchKeyword = ref("");
const searchResults = ref([]);
const selectedMovie = ref(null);
const watchedDate = ref("");
const isSearching = ref(false);
const isSaving = ref(false);

const props = defineProps(["id"]);

const API_KEY =
  "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YjI0YzA4NjJkNTQwODFmYjE0Y2VhZGMwMWZkODI4MCIsIm5iZiI6MTczMTY0NzQ1Ni42NDg5MzUzLCJzdWIiOiI2NzM2ZDc0MWZmZTM4NzhlOWU5ZmFmYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.eYQu1H6KBYqKX0e-WvHcWIH3AT1ioH1j-4OmFLxxUxk";

// 실시간 영화 검색 (디바운스 적용)
watch(
  searchKeyword,
  debounce(async (newQuery) => {
    if (!newQuery.trim()) {
      searchResults.value = [];
      return;
    }

    isSearching.value = true;
    try {
      const response = await axios({
        method: "get",
        url: "https://api.themoviedb.org/3/search/movie",
        params: {
          query: newQuery,
          language: "ko-KR",
        },
        headers: {
          Authorization: API_KEY,
        },
      });
      searchResults.value = response.data.results;
    } catch (error) {
      console.error("영화 검색 실패:", error);
    } finally {
      isSearching.value = false;
    }
  }, 300)
);

// 영화 선택
const selectMovie = (movie) => {
  selectedMovie.value = movie;
  searchResults.value = [];
  searchKeyword.value = "";
};

// handleSubmit 함수
const handleSubmit = () => {
  if (!selectedMovie.value || !watchedDate.value) return;

  isSaving.value = true;

  // console.log("전송할 데이터:", movieData); // 디버깅용

  console.log(selectedMovie.value);
  console.log(watchedDate.value);
  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/groups/${props.id}/movies/`,
    data: {
      movie_data: selectedMovie.value,
      watched_date: watchedDate.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("영화 등록 성공:", response.data);
      emit("group-movie-created");
      emit("close");
    })
    .catch((error) => {
      console.error("영화 등록 실패:", error.response?.data || error);
      if (error.response?.data) {
        console.log("서버 에러 메시지:", error.response.data); // 상세 에러 확인
      }
      alert("영화 등록에 실패했습니다. 다시 시도해주세요.");
    })
    .finally(() => {
      isSaving.value = false;
    });
};

const emit = defineEmits(["close", "group-movie-created"]);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  padding: 2.5rem;
  border-radius: 4px;
  width: 90%;
  max-width: 550px;
  max-height: 85vh;
  overflow-y: auto;
}

.modal-content h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 2rem;
  text-align: center;
}

.form-group {
  margin-bottom: 2rem;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 600;
  font-size: 1rem;
  color: #1a1a1a;
}

.form-group input {
  width: 100%;
  padding: 0.875rem 1.25rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: all 0.2s;
}

.form-group input:focus {
  border-color: #3a3a3a;
  outline: none;
}

/* 캘린더 input 스타일 개선 */
input[type="date"] {
  appearance: none;
  background: white;
  cursor: pointer;
  padding-right: 2.5rem;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='4' width='18' height='18' rx='2' ry='2'%3E%3C/rect%3E%3Cline x1='16' y1='2' x2='16' y2='6'%3E%3C/line%3E%3Cline x1='8' y1='2' x2='8' y2='6'%3E%3C/line%3E%3Cline x1='3' y1='10' x2='21' y2='10'%3E%3C/line%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  opacity: 0;
  cursor: pointer;
  position: absolute;
  right: 0;
  top: 0;
  width: 100%;
  height: 100%;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 0.5rem;
  background: white;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-height: 300px;
  overflow-y: auto;
  z-index: 10;
}

.search-item {
  display: flex;
  padding: 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s;
}

.search-item:last-child {
  border-bottom: none;
}

.search-item:hover {
  background: #f8f9fa;
}

.search-item img {
  width: 46px;
  height: 69px;
  object-fit: cover;
  margin-right: 1rem;
  border-radius: 4px;
}

.movie-details {
  flex: 1;
}

.movie-title {
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 0.25rem 0;
}

.movie-year {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.selected-movie {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 4px;
  text-align: center;
}

.selected-movie img {
  width: 180px;
  border-radius: 4px;
  margin-bottom: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.selected-movie h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2.5rem;
}

.button-group button {
  padding: 0.875rem 2rem;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 120px;
}

.cancel-btn {
  background: #f5f5f5;
  border: none;
  color: #666;
}

.cancel-btn:hover {
  background: #e5e5e5;
}

.submit-btn {
  background: #3a3a3a;
  color: white;
  border: none;
}

.submit-btn:not(:disabled):hover {
  background: #2a2a2a;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 스크롤바 스타일 */
.modal-content::-webkit-scrollbar,
.search-results::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track,
.search-results::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.modal-content::-webkit-scrollbar-thumb,
.search-results::-webkit-scrollbar-thumb {
  background: #888;
}

/* 로딩 스피너 */
.spinner-border {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 0.2em solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner-border 0.75s linear infinite;
}

@keyframes spinner-border {
  to {
    transform: rotate(360deg);
  }
}

.me-2 {
  margin-right: 0.5rem;
}

@media (max-width: 768px) {
  .modal-content {
    padding: 1.5rem;
  }

  .selected-movie img {
    width: 150px;
  }

  .button-group button {
    padding: 0.75rem 1.5rem;
  }
}
</style>
