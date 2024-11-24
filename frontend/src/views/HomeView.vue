<!-- HomeView -->
<template>
  <div class="home-container">
    <br />
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
            <!--  ******* 장르 모델 경로 변경 후 확인 *******-->
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
                    <!--  ******* 장르 데이터 속성으로 적용 필요 *******-->
                    <span>{{ movie.genre }}</span>
                  </div>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 검색창 영역 -->
    <div class="search-section">
      <div class="search-container">
        <!-- 검색창 -->
        <input type="text" :value="groupKeyword" @input="handleSearchGroups" placeholder="그룹명을 입력하세요." class="search-btn" />
        <!-- 그룹 필터 -->
        <select v-model="selectedCategory" class="category-dropdown" @change="filterGroups">
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
        <!-- 그룹 생성 버튼 -->
        <button @click="openModal" class="create-group-btn">그룹생성</button>
      </div>

      <!-- 모달 컴포넌트 -->
      <Transition name="modal">
        <GroupCreateModal v-if="isModalOpen" @close="closeModal" @group-created="onGroupCreated" />
      </Transition>
    </div>

    <main class="main-content">
      <!-- 그룹 그리드 -->
      <div class="groups-grid">
        <div v-for="group in filteredGroups" :key="group.id" :id="group.id" class="group-card">
          <RouterLink :to="{ name: 'GroupDetailView', params: { group_id: group.id } }">
            <div class="group-image-container">
              <img :src="'http://127.0.0.1:8000' + group.group_img" :alt="group.group_name" class="group-image" />
              <div
                class="group-type"
                :class="{
                  'category-family': getCategoryName(group.category) === '가족',
                  'category-couple': getCategoryName(group.category) === '연인',
                  'category-friend': getCategoryName(group.category) === '친구',
                  'category-work': getCategoryName(group.category) === '직장',
                  'category-ssafy': getCategoryName(group.category) === 'SSAFY',
                  'category-etc': getCategoryName(group.category) === '기타',
                }"
              >
                {{ getCategoryName(group.category) }}
              </div>
            </div>

            <div class="group-info">
              <div class="group-header">
                <h3 class="group-name">{{ group.group_name }}</h3>
                <div class="activity-badge" :class="group.activityLevel">
                  {{ group.activityLevel }}
                </div>
              </div>

              <p class="group-description">{{ group.description }}</p>

              <!-- 카드에서 멤버와 영화(몇 편 봤는지) 부분 -->
              <div class="group-stats">
                <div class="stats-left">
                  <div class="stats-item">
                    <span class="stats-label">영화</span>
                    <span class="stats-value">{{ group.postCount }}</span>
                  </div>
                </div>

                <div class="stats-right">
                  <div class="member-avatars">
                    <img v-for="(member, index) in group.include_members.slice(0, 3)" :key="member.id" :src="'http://127.0.0.1:8000' + member.profile_img" :alt="member.name" class="member-avatar" />
                    <span v-if="group.include_members.length > 3" class="left-member-count stats-value ml-2">+{{ group.include_members.length - 3 }}</span>
                  </div>
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
import axios from "axios";
import { ref, onMounted, watch } from "vue";
import { useRouter, RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import GroupCreateModal from "@/components/GroupCreateModal.vue";

// 상태 관리
const recommendedMovies = ref([]);
const loadingMovies = ref(true);
const movieError = ref(null);
// - 검색 상태 관리
const groupKeyword = ref("");
console.log(groupKeyword.value);

const categories = [
  { id: "0", name: "전체" },
  { id: "1", name: "가족" },
  { id: "2", name: "연인" },
  { id: "3", name: "친구" },
  { id: "4", name: "직장" },
  { id: "5", name: "SSAFY" },
  { id: "6", name: "기타" },
];

// 카테고리 ID를 이름으로 변환하는 함수
const getCategoryName = (categoryId) => {
  const category = categories.find((cat) => cat.id === categoryId);
  return category ? category.name : "기타";
};

// 선택된 카테고리 초기값 설정
const selectedCategory = ref("0");

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
  // ******* axios 요청 경로 은영이 모델 재설계 후 확인 *******
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

// 그룹 데이터 가져오기
const allGroups = ref([]);
const filteredGroups = ref([]);

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
      // 기존 데이터 초기화
      allGroups.value = [];
      filteredGroups.value = [];

      // 그룹별 멤버 정보를 받아오기 위해서 그룹 상세 정보 api를 다시 호출
      response.data.map((group, index) => {
        axios({
          method: "get",
          url: `${store.API_URL}/api/v1/groups/${group.id}/`,
          headers: {
            Authorization: `Token ${store.token}`,
          },
        })
          .then((response) => {
            allGroups.value.push(response.data);
            filteredGroups.value = allGroups.value;
          })
          .catch((error) => {
            console.error("그룹 상세 데이터 가져오기 실패:", error);
          });
      });
    })
    .catch((error) => {
      console.error("그룹 데이터 가져오기 실패:", error);
    });
};

const filterGroups = () => {
  // 그룹 필터링
  filteredGroups.value = allGroups.value.filter((group) => {
    const nameMatches = group.group_name.toLowerCase().includes(groupKeyword.value.toLowerCase());
    const categoryMatches = selectedCategory.value === "0" || group.category === selectedCategory.value;
    return nameMatches && categoryMatches;
  });
};

const handleSearchGroups = (event) => {
  groupKeyword.value = event.currentTarget.value;
  filterGroups();
};

onMounted(() => {
  fetchRecommendedMovies();
  getGroupData();
});

const onGroupCreated = () => {
  closeModal(); // 모달 닫기
  getGroupData(); // 그룹 목록 새로고침
};
</script>

<style scoped>
/* 전체 컨테이너 */
.home-container {
  max-width: 1300px;
  margin: 0 auto;
  /* padding: 0 auto; */
}

.main-title {
  font-size: 2rem;
  font-weight: 700;
  color: #3a3a3a;
  position: relative;
  margin-bottom: 1rem;
}
.main-title::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -0.5rem;
  width: 50px;
  height: 3px;
  background: #dc3545;
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

/* 검색 섹션 */
.search-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-btn {
  flex: 1;
  height: 50px;
  border: none;
  border-radius: 10px;
  text-align: left;
  padding-left: 20px;
  background-color: #f5f5f5;
}

.search-btn:hover {
  background-color: #ebebeb;
}

.search-btn:focus {
  outline: none;
}

.create-group-btn {
  padding: 8px 16px;
  height: 50px;
  background-color: #3a3a3a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.create-group-btn:hover {
  background-color: #3a3a3a;
}

/* 메인 컨텐츠 영역 */
.main-content {
  padding-top: 64px;
  max-width: 1300px;
  margin: 0 auto;
}

/* 필터 섹션 */
.filter-section {
  padding: 0 2rem;
  margin-bottom: 3rem;
  display: flex;
  justify-content: center;
}

.category-dropdown {
  height: 50px;
  padding: 0 2rem;
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
  border-color: #3a3a3a;
}

.category-dropdown:focus {
  outline: none;
  border-color: #3a3a3a;
  box-shadow: 0 0 0 2px 3a3a3a;
}

/* 카테고리 색상 스타일 추가 */
.category-family {
  background-color: #e9fae9 !important;
  color: #2c7a2c !important;
}

.category-couple {
  background-color: #fae9e9 !important;
  color: #7a2c2c !important;
}

.category-friend {
  background-color: #e9eafa !important;
  color: #2c2c7a !important;
}

.category-work {
  background-color: #faf6e9 !important;
  color: #7a672c !important;
}

.category-ssafy {
  background-color: #f2e9fa !important;
  color: #672c7a !important;
}

.category-etc {
  background-color: #e9fafa !important;
  color: #2c7a7a !important;
}

/* 그룹 그리드 */
.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  /* padding: 0 2rem; */
  margin-bottom: 4rem;
}

.group-card {
  background: #ffffff;
  overflow: hidden;
  transition: transform 0.2s ease;
  border: 1px solid #e6e3e1;
  border-radius: 8px;
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
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
  font-weight: 500;
  border-radius: 4px;
  /* 배경색과 텍스트 색상은 위의 카테고리 클래스에서 지정됨 */
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
  color: #3a3a3a;
  letter-spacing: -0.5px;
}

.group-description {
  font-size: 0.9rem;
  color: #666666;
  margin-bottom: 1.5rem;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.group-stats {
  display: flex;
  gap: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e6e3e1;
  align-items: center;
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

/* 활동 배지 */
.activity-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* 모달 트랜지션 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .movie-card {
    width: 150px;
  }

  .movie-image-container {
    height: 210px;
  }

  .search-container {
    flex-direction: column;
    gap: 10px;
  }

  .search-btn {
    width: 100%;
  }

  .create-group-btn {
    width: 100%;
  }

  .groups-grid {
    grid-template-columns: 1fr;
    padding: 0 1rem;
  }

  .group-image-container {
    height: 180px;
  }

  .category-dropdown {
    width: 90%;
    max-width: 300px;
  }

  .filter-section {
    padding: 0 1rem;
  }
}

a {
  text-decoration: none;
}
.member-avatars {
  display: flex;
  align-items: center;

  .left-member-count {
    margin-left: 10px;
  }
}

.member-avatar {
  width: 40px;
  border-radius: 30px;
  border: 4px white solid;
  /* margin: 0px; */
  margin: -5px;
}
</style>
