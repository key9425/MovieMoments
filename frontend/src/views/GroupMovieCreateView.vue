<template>
  <div class="container mt-5">
    <div class="text-center mb-4">
      <h1 class="display-5 mb-3">그룹 영화 등록</h1>
      <p class="text-muted">{{ groupName }}에서 함께 본 영화를 기록하세요!</p>
    </div>
 
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-body">
            <form @submit.prevent="saveGroupMovie">
              <!-- 영화 검색 -->
              <div class="mb-4">
                <label class="form-label">영화 선택</label>
                <div class="search-area">
                  <div class="position-relative">
                    <input 
                      type="text" 
                      class="form-control" 
                      v-model="searchKeyword"
                      placeholder="영화 제목을 입력하세요"
                      :class="{ 'is-searching': isSearching }"
                    />
                    <div v-if="isSearching" class="searching-indicator">
                      <div class="spinner-border spinner-border-sm text-primary" role="status">
                        <span class="visually-hidden">검색중...</span>
                      </div>
                    </div>
                  </div>
                </div>
 
                <!-- 검색 결과 -->
                <div v-if="searchResults.length" class="search-results mb-3">
                  <div 
                    v-for="movie in searchResults" 
                    :key="movie.id" 
                    class="movie-item"
                    :class="{ selected: selectedMovie?.id === movie.id }"
                    @click="selectMovie(movie)"
                  >
                    <img 
                      :src="movie.poster_path ? `https://image.tmdb.org/t/p/w92${movie.poster_path}` : '/no-poster.jpg'"
                      :alt="movie.title" 
                      class="movie-poster"
                    />
                    <div class="movie-info">
                      <h5 class="mb-1">{{ movie.title }}</h5>
                      <p class="text-muted mb-0">{{ new Date(movie.release_date).getFullYear() }}</p>
                    </div>
                  </div>
                </div>
              </div>
 
              <!-- 선택된 영화 표시 -->
              <div v-if="selectedMovie" class="selected-movie mb-4">
                <h5>선택된 영화</h5>
                <div class="d-flex align-items-center gap-3 p-3 bg-light rounded">
                  <img 
                    :src="`https://image.tmdb.org/t/p/w92${selectedMovie.poster_path}`"
                    :alt="selectedMovie.title"
                    class="rounded"
                    width="60"
                  />
                  <div>
                    <h6 class="mb-1">{{ selectedMovie.title }}</h6>
                    <p class="mb-0 text-muted">{{ new Date(selectedMovie.release_date).getFullYear() }}</p>
                  </div>
                </div>
              </div>
 
              <!-- 관람일 선택 -->
              <div class="mb-4">
                <label for="watchedDate" class="form-label">관람일</label>
                <input 
                  type="date" 
                  class="form-control" 
                  id="watchedDate"
                  v-model="watchedDate"
                  required
                />
              </div>
 
              <!-- 제출 버튼 -->
              <div class="d-grid">
                <button 
                  type="submit" 
                  class="btn btn-primary"
                  :disabled="!selectedMovie || !watchedDate || isSaving"
                >
                  <span v-if="isSaving" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  {{ isSaving ? '저장중...' : '등록하기' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
 </template>
 
 <script setup>
 import { ref, watch, onMounted } from 'vue';
 import { useRoute, useRouter } from 'vue-router';
 import { useCounterStore } from '@/stores/counter';
 import axios from 'axios';
 import { debounce } from 'lodash';
 
 const route = useRoute();
 const router = useRouter();
 const store = useCounterStore();
 
 const groupName = ref('');
 const searchKeyword = ref('');
 const searchResults = ref([]);
 const selectedMovie = ref(null);
 const watchedDate = ref('');
 const isSearching = ref(false);
 const isSaving = ref(false);
 
 const API_KEY = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YjI0YzA4NjJkNTQwODFmYjE0Y2VhZGMwMWZkODI4MCIsIm5iZiI6MTczMTY0NzQ1Ni42NDg5MzUzLCJzdWIiOiI2NzM2ZDc0MWZmZTM4NzhlOWU5ZmFmYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.eYQu1H6KBYqKX0e-WvHcWIH3AT1ioH1j-4OmFLxxUxk';
 
 // 실시간 영화 검색 (디바운스 적용)
 watch(searchKeyword,
  debounce(async (newQuery) => {
    if (!newQuery.trim()) {
      searchResults.value = [];
      return;
    }
 
    isSearching.value = true;
    try {
      const response = await axios({
        method: 'get',
        url: 'https://api.themoviedb.org/3/search/movie',
        params: {
          query: newQuery,
          language: 'ko-KR'
        },
        headers: {
          Authorization: API_KEY
        }
      });
      searchResults.value = response.data.results;
    } catch (error) {
      console.error('영화 검색 실패:', error);
    } finally {
      isSearching.value = false;
    }
  }, 300)
 );
 
 // 영화 선택
 const selectMovie = (movie) => {
  selectedMovie.value = movie;
  searchResults.value = [];
  searchKeyword.value = '';
 };
 
 // 그룹 영화 저장
 const saveGroupMovie = async () => {
  if (!selectedMovie.value || !watchedDate.value) return;

  isSaving.value = true;
  try {
    const response = await axios({
      method: "post",
      url: `${store.API_URL}/api/v1/groups/${route.params.group_id}/movies/`,
      data: {
        movie_data: selectedMovie.value,  // 영화 전체 정보 전송
        watched_date: watchedDate.value,
      },
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    console.log("영화 등록 성공:", response.data);
    // router.push({ name: "GroupDetail", params: { groupId: route.params.groupId } });
  } catch (error) {
    console.error("영화 등록 실패:", error);
    alert("영화 등록에 실패했습니다. 다시 시도해주세요.");
  } finally {
    isSaving.value = false;
  }
};
 </script>
 
 <style scoped>
 .movie-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
 }
 
 .movie-item:hover {
  background-color: #f8f9fa;
 }
 
 .movie-item.selected {
  background-color: #e3f2fd;
 }
 
 .movie-poster {
  width: 60px;
  height: 90px;
  object-fit: cover;
 }
 
 .search-results {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #dee2e6;
  border-radius: 4px;
 }
 
 .searching-indicator {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
 }
 
 .is-searching {
  padding-right: 40px;
 }
 
 .selected-movie img {
  object-fit: cover;
 }
 </style>