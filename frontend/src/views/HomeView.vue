<!-- HomeView -->
<template>
  <div class="home-container">
    <h1>Home page</h1>
    <br />
    <h2>오늘의 추천영화</h2>
    <div class="recommended-movies">
      <div v-if="loadingMovies" class="text-center py-4">로딩 중...</div>
      <div v-else-if="movieError" class="text-red-500 py-4">
        {{ movieError }}
      </div>
      <div v-else class="movies-grid">
        <div v-for="movie in recommendedMovies" :key="movie.id" class="movie-card">
          <div class="movie-image-container">
            <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" :alt="movie.title" class="movie-image" />
          </div>
          <div class="movie-info">
            <h3 class="movie-title">{{ movie.title }}</h3>
          </div>
        </div>
      </div>
    </div>
    <form>
      <input type="text" placeholder="그룹검색" class="search-btn" />
    </form>

    <button @click="openModal" class="create-group-btn">그룹생성</button>

    <!-- 모달 컴포넌트에 트랜지션 추가 -->
    <Transition name="modal">
      <GroupCreateModal v-if="isModalOpen" @close="closeModal" @group-created="onGroupCreated" />
    </Transition>

    <main class="main-content">
      <!-- 그룹 필터 -->
      <div class="filter-section">
        <select v-model="selectedCategory" class="category-dropdown" @change="filterGroups">
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>

      <!-- 그룹 그리드 -->
      <div class="groups-grid">
        <div v-for="group in filteredGroups" :key="group.id" :id="group.id" class="group-card">
          <RouterLink :to="{ name: 'GroupDetailView', params: { group_id: group.id } }">
            <div class="group-image-container">
              <img :src="'http://127.0.0.1:8000' + group.group_img" :alt="group.group_name" class="group-image" />
              <div class="group-type">{{ group.category }}</div>
            </div>
            <div class="group-info">
              <div class="group-header">
                <h3 class="group-name">{{ group.group_name }}</h3>
                <div class="activity-badge" :class="group.activityLevel">
                  {{ group.activityLevel }}
                </div>
              </div>
              <p class="group-description">{{ group.description }}</p>
              <div class="group-stats">
                <div class="stats-item">
                  <span class="stats-label">멤버</span>
                  <span class="stats-value">{{ group.memberCount }}</span>
                </div>
                <div class="stats-item">
                  <span class="stats-label">게시글</span>
                  <span class="stats-value">{{ group.postCount }}</span>
                </div>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, RouterLink } from "vue-router";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import GroupCreateModal from "@/components/GroupCreateModal.vue";

// 상태 관리
const recommendedMovies = ref([]);
const loadingMovies = ref(true);
const movieError = ref(null);

const selectedCategory = ref("1");
const categories = ["1", "2", "3", "4", "5", "6"];
const isModalOpen = ref(false);

const router = useRouter();
const store = useCounterStore();
const API_URL = store.API_URL;

const openModal = () => {
  isModalOpen.value = true;
  document.body.style.overflow = "hidden";
};

const closeModal = () => {
  isModalOpen.value = false;
  document.body.style.overflow = "auto";
};

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

// 그룹 데이터 가져오기
const allGroups = ref([]);
const getGroupData = () => {
  axios({
    method: "get",
    url: `${API_URL}/api/v1/groups/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("response = ", response);
      allGroups.value = response.data;
    })
    .catch((error) => {
      console.error("그룹 데이터 가져오기 실패:", error);
    });
};

onMounted(() => {
  getGroupData();
});

// 필터링된 그룹 computed 속성
const filteredGroups = computed(() => {
  if (selectedCategory.value === "1") {
    return allGroups.value;
  }
  return allGroups.value.filter((group) => group.category === selectedCategory.value);
});

const onGroupCreated = () => {
  closeModal(); // 모달 닫기
  getGroupData(); // 그룹 목록 새로고침
};
</script>

<style scoped>
.home-container {
  background-color: #ffffff;
  min-height: 100vh;
  color: #4a4a4a;
}

/* 그룹 생성 버튼 스타일 */
.create-group-btn {
  padding: 8px 16px;
  background-color: #635985;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  margin: 20px;
}

.create-group-btn:hover {
  background-color: #524a6e;
}

/* 검색 버튼 스타일 */
.search-btn {
  width: 1000px;
  height: 50px;
  border: none;
  border-radius: 10px;
  text-align: left;
  display: block;
  margin: 30px auto;
  padding-left: 20px;
  background-color: #f5f5f5;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #ebebeb;
}

/* 모달 트랜지션 효과 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.main-content {
  padding-top: 64px;
  max-width: 1200px;
  margin: 0 auto;
}

.filter-section {
  padding: 0 2rem;
  margin-bottom: 3rem;
  display: flex;
  justify-content: center;
}

.category-dropdown {
  padding: 0.8rem 2rem;
  font-size: 0.95rem;
  border: 1px solid #e6e3e1;
  border-radius: 8px;
  background-color: white;
  color: #666666;
  cursor: pointer;
  min-width: 150px;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  transition: all 0.2s ease;
}

.category-dropdown:hover {
  border-color: #635985;
}

.category-dropdown:focus {
  outline: none;
  border-color: #635985;
  box-shadow: 0 0 0 2px rgba(99, 89, 133, 0.1);
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  padding: 0 2rem;
  margin-bottom: 4rem;
}

.group-card {
  background: #ffffff;
  overflow: hidden;
  transition: transform 0.2s ease;
  border: 1px solid #e6e3e1;
}

.group-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
}

.group-image-container {
  position: relative;
  height: 200px;
}

.group-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.group-type {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background-color: rgba(255, 255, 255, 0.95);
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: #635985;
}

.group-info {
  padding: 1.5rem;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.8rem;
}

.group-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333333;
  letter-spacing: -0.5px;
}

.group-description {
  font-size: 0.9rem;
  color: #666666;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.group-stats {
  display: flex;
  gap: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e6e3e1;
}

.stats-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.stats-label {
  font-size: 0.8rem;
  color: #8b8b8b;
  font-weight: 500;
}

.stats-value {
  font-size: 1rem;
  color: #333333;
  font-weight: 600;
}
/* 추천 영화 섹션 스타일 */
.recommended-movies {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.movie-card {
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s ease;
  border: 1px solid #e6e3e1;
}

.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
}

.movie-image-container {
  position: relative;
  height: 270px;
}

.movie-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-info {
  padding: 1rem;
}

.movie-title {
  font-size: 1rem;
  font-weight: 600;
  color: #333333;
  margin-bottom: 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.movie-rating {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.rating-star {
  color: #ffd700;
}

.rating-value {
  font-size: 0.9rem;
  color: #666666;
}

@media (max-width: 768px) {
  .search-btn {
    width: 90%;
    margin: 20px auto;
  }

  .category-dropdown {
    width: 90%;
    max-width: 300px;
  }

  .groups-grid {
    padding: 0 1rem;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  }
  .recommended-movies {
    padding: 0 1rem;
  }

  .movies-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 1rem;
  }

  .movie-image-container {
    height: 210px;
  }
}
</style>
