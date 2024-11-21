<!-- HomeView -->
<template>
  <div>
    <h1>Home page</h1>
    <br />
    <form>
      <input type="text" placeholder="그룹검색" />
    </form>

    <button @click="goGroupCreate">그룹생성</button>

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

// 상태 관리
const selectedCategory = ref("1");
const categories = ["1", "2", "3", "4", "5", "6"];

// 그룹 생성 버튼 후 그룹 생성 페이지로 이동
const router = useRouter();
const store = useCounterStore();
const API_URL = store.API_URL;

const goGroupCreate = () => {
  router.push({ name: "GroupCreateView" });
};

// const allGroups = ref([
//   {
//     id: 1,
//     name: "시간을 기록하는 사람들",
//     description: "일상의 특별한 순간을 글과 사진으로 남기는 모임",
//     type: "문화",
//     memberCount: "287",
//     postCount: "1.2k",
//     activityLevel: "활발",
//     image: "https://via.placeholder.com/400x300",
//   },
// ]);

// // 그룹디테일로 이동하기
// const goGroupDetail = () => {
//   router.push({ name: "GroupDetailView" });
// };

// 그룹 데이터 가져오기
const allGroups = ref([]);
const getGroupData = () => {
  axios({
    method: "get",
    url: `${API_URL}/api/v1/groups/`,
    headers: {
      Authorization: `Token ${store.token}`, // 토큰 추가
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
</script>

<style scoped>
.app-container {
  /* background-color: #f8f7f6; 따뜻한 베이지 배경 */
  background-color: #ffffff;
  min-height: 100vh;
  color: #4a4a4a;
}

.navigation {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #fffefc; /* 밝은 베이지 */
  padding: 1rem 0;
  border-bottom: 1px solid #e6e3e1;
  z-index: 1000;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.site-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #635985; /* 부드러운 보라색 */
  letter-spacing: -0.5px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 2.5rem;
}

.nav-link {
  text-decoration: none;
  color: #666666;
  font-size: 0.95rem;
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: #635985; /* 부드러운 보라색 */
}

.profile-button {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid #e6e3e1;
}

.profile-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.main-content {
  padding-top: 64px;
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  padding: 4rem 2rem;
  text-align: center;
  position: relative;
}

.header-line {
  width: 40px;
  height: 2px;
  background-color: #635985; /* 부드러운 보라색 */
  margin: 0 auto 1.5rem;
}

.welcome-text {
  font-size: 1.8rem;
  font-weight: 600;
  color: #443c68; /* 진한 보라그레이 */
  margin-bottom: 0.5rem;
  letter-spacing: -0.5px;
}

.date-text {
  color: #8b8b8b;
  font-size: 1rem;
  font-weight: 500;
}

/* 드롭다운 스타일 */
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
  appearance: none; /* 기본 화살표 제거 */
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

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.filter-button {
  padding: 0.6rem 1.2rem;
  border: none;
  background: #ffffff;
  color: #666666;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-button:hover {
  background-color: #635985; /* 부드러운 보라색 */
  color: white;
}

.filter-button.active {
  background-color: #635985; /* 부드러운 보라색 */
  color: white;
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
  color: #635985; /* 부드러운 보라색 */
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

/* 검색 버튼 스타일을 미디어 쿼리 밖으로 이동하고 수정 */
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

@media (max-width: 768px) {
  .nav-content {
    padding: 0 1rem;
  }

  .header-section {
    padding: 2rem 1rem;
  }

  .welcome-text {
    font-size: 1.5rem;
  }

  .filter-section {
    padding: 0 1rem;
  }

  /* .filter-buttons {
    overflow-x: auto;
    padding-bottom: 1rem;
  } */
  .filter-section {
    padding: 0 1rem;
  }

  .category-dropdown {
    width: 90%;
    max-width: 300px;
  }

  .groups-grid {
    padding: 0 1rem;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  }

  /* 모바일에서의 검색 버튼 스타일 조정 */
  .search-btn {
    width: 90%; /* 모바일에서는 화면 너비의 90%로 조정 */
    margin: 20px auto;
  }
}
</style>
