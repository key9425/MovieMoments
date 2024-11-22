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
                <p class="movie-year">{{ movie.release_date?.split("-")[0] }}</p>
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-results {
  margin-top: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
}

.search-item {
  display: flex;
  padding: 0.5rem;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.search-item:hover {
  background: #f5f5f5;
}

.search-item img {
  width: 46px;
  height: 69px;
  object-fit: cover;
  margin-right: 1rem;
}

.selected-movie {
  margin: 1rem 0;
  text-align: center;
}

.selected-movie img {
  width: 150px;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.button-group button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn {
  background: #f5f5f5;
  border: 1px solid #ddd;
}

.submit-btn {
  background: #3a3a3a;
  color: white;
  border: none;
}

.submit-btn:hover {
  background: #2a2a2a;
}
/* style 부분에 추가 */
.spinner-border {
  width: 1rem;
  height: 1rem;
  border-width: 0.2em;
}

.button-group button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.me-2 {
  margin-right: 0.5rem;
}

.spinner-border-sm {
  --bs-spinner-width: 1rem;
  --bs-spinner-height: 1rem;
  --bs-spinner-border-width: 0.2em;
}
</style>
