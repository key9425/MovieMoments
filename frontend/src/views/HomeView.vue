<!-- HomeView -->
<template>
  <div class="home-container">
    <br />
    <!-- 상단 제목 -->
    <!-- <section>
      <div class="header-section">
        <h2 class="main-title">오늘의 추천 영화</h2>
      </div>
    </section> -->

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
          <button v-if="canSlidePrev" class="carousel-button prev" @click="slide('prev')">
            <i class="fas fa-chevron-left"></i>
          </button>
          <div class="carousel-wrapper" :style="{ width: `${carouselConfig.totalWidth}px` }">
            <div
              class="movie-carousel"
              :style="{
                transform: `translateX(-${currentSlide * (CARD_WIDTH + CARD_GAP)}px)`,
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
          <button v-if="canSlideNext" class="carousel-button next" @click="slide('next')">
            <i class="fas fa-chevron-right"></i>
          </button>
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
                    <span class="stats-label">영화: {{ group.watched_movies.length }}</span>
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
import { ref, onMounted, computed, onBeforeUnmount, watch } from "vue";
import { useRouter, RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import GroupCreateModal from "@/components/GroupCreateModal.vue";
import { debounce } from "lodash";

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

watch(filteredGroups, () => {
  console.log("filtered group", filteredGroups.value);
});

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

// 케러셀 관련 상수
const CARD_WIDTH = 224; // 카드 기본 너비
const CARD_GAP = 20; // 카드 간격
const CONTAINER_PADDING = 32; // 컨테이너 좌우 패딩

// 케러셀 상태
const currentSlide = ref(0);
const carouselConfig = ref(null);

// 슬라이드 가능 여부 계산
const canSlidePrev = computed(() => currentSlide.value > 0);
const canSlideNext = computed(() => {
  if (!carouselConfig.value || !recommendedMovies.value) return false;
  return currentSlide.value < Math.max(0, recommendedMovies.value.length - carouselConfig.value.cardsPerView);
});

// 화면 크기에 따른 카드 수와 너비 계산
const calculateArea = () => {
  const containerWidth = Math.min(window.innerWidth - CONTAINER_PADDING, 1300);

  // 표시 가능한 최대 카드 수 계산
  const possibleCards = Math.floor(containerWidth / (CARD_WIDTH + CARD_GAP));

  // 실제 케러셀 너비 계산
  const carouselWidth = possibleCards * CARD_WIDTH + (possibleCards - 1) * CARD_GAP;

  return {
    cardsPerView: possibleCards,
    cardWidth: CARD_WIDTH,
    totalWidth: carouselWidth,
  };
};

// 슬라이드 이동 함수
const slide = (direction) => {
  if (direction === "next" && canSlideNext.value) {
    currentSlide.value++;
  } else if (direction === "prev" && canSlidePrev.value) {
    currentSlide.value--;
  }
};

// 화면 크기 변경 감지
const handleResize = debounce(() => {
  carouselConfig.value = calculateArea();

  // 현재 슬라이드 위치 재조정
  const maxSlide = Math.max(0, recommendedMovies.value.length - carouselConfig.value.cardsPerView);
  if (currentSlide.value > maxSlide) {
    currentSlide.value = maxSlide;
  }
}, 200);

const onGroupCreated = () => {
  closeModal(); // 모달 닫기
  getGroupData(); // 그룹 목록 새로고침
};

onMounted(() => {
  window.addEventListener("resize", handleResize);
  carouselConfig.value = calculateArea();
  fetchRecommendedMovies();
  getGroupData();
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
});
</script>

<style scoped>
/* 전체 컨테이너 */
.home-container {
  /* max-width: 1300px; */
  background-color: #f8f9fa;
  margin: 0 auto;
}

/* 추천 영화 섹션 스타일 */
.movie-section {
  background-color: #1a1a1a;
  margin: -2rem 0 0 0;
  padding: 4rem 0;
}

.content-wrapper {
  max-width: 1300px;
  margin: 0 auto;
}

.section-title {
  color: white;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  position: relative;
}

.section-title::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -0.5rem;
  width: 60px;
  height: 4px;
  background: #ffd700;
}

/* 캐러셀 스타일 */
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
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  overflow: hidden;
  transform-origin: center bottom;
  transition: all 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
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
  transition: transform 0.3s ease;
}

.movie-card:hover .movie-poster {
  transform: scale(1.05);
}

.movie-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 30%, rgba(0, 0, 0, 0.8) 100%);
  opacity: 0;
  transition: opacity 0.2s;
  display: flex;
  align-items: flex-end;
  padding: 1rem;
}

.movie-card:hover .movie-overlay {
  opacity: 1;
}

.movie-info {
  padding: 0;
}

.movie-info h3 {
  color: #ffd700;
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
  text-wrap: balance;
}

.movie-meta {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 0.25rem;
}

/* 캐러셀 네비게이션 버튼 */
.carousel-button {
  position: absolute;
  top: 50%;
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

/* 로딩 및 에러 상태 */
.loading-state {
  text-align: center;
  padding: 2rem;
  color: white;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.2);
  border-top: 3px solid #ffd700;
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

.error-state {
  text-align: center;
  padding: 2rem;
  color: #dc3545;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 검색 섹션 */
.search-section {
  max-width: 1200px;
  margin: 20px auto 0;
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
  background-color: #ebebeb;
}

.search-btn:hover {
  background-color: #d8d8d8;
}

.search-btn:focus {
  outline: none;
}

.create-group-btn {
  padding: 8px 16px;
  height: 50px;
  background-color: #4a4a4a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.create-group-btn:hover {
  background-color: #dc3545;
}

/* 메인 컨텐츠 영역 */
.main-content {
  padding-top: 64px;
  max-width: 1300px;
  margin: 0 auto;
}

/* 카테고리 필터 */
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
  box-shadow: 0 0 0 2px rgba(58, 58, 58, 0.2);
}

/* 그룹 그리드 */
.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

/* 멤버 아바타 */
.member-avatars {
  display: flex;
  align-items: center;
}

.member-avatar {
  width: 40px;
  border-radius: 30px;
  border: 4px white solid;
  margin: -5px;
}

.left-member-count {
  margin-left: 10px;
}

/* 카테고리 색상 */
.category-family {
  background-color: #e9fae9;
  color: #2c7a2c;
}

.category-couple {
  background-color: #fae9e9;
  color: #7a2c2c;
}

.category-friend {
  background-color: #e9eafa;
  color: #2c2c7a;
}

.category-work {
  background-color: #faf6e9;
  color: #7a672c;
}

.category-ssafy {
  background-color: #f2e9fa;
  color: #672c7a;
}

.category-etc {
  background-color: #e9fafa;
  color: #2c7a7a;
}

/* 그룹 카드 스타일 */
.group-card {
  background: #ffffff;
  border: 1px solid #e6e3e1;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s ease;
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
  justify-content: space-between;
  align-items: center;
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

/* 모달 트랜지션 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* 링크 스타일 */
a {
  text-decoration: none;
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
  .movie-section {
    padding: 3rem 0;
  }

  .section-title {
    font-size: 1.6rem;
  }

  .search-container {
    flex-direction: column;
    gap: 10px;
  }

  .search-btn,
  .create-group-btn {
    width: 100%;
  }

  .carousel-button {
    width: 36px;
    height: 36px;
    font-size: 1rem;
  }

  .movie-info h3 {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.8rem;
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
