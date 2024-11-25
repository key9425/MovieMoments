<template>
  <nav class="navigation">
    <div class="nav-container">
      <div class="nav-left">
        <RouterLink :to="{ name: 'HomeView' }" class="site-title">영화처럼, 순간처럼</RouterLink>
        <div class="nav-links">
          <RouterLink :to="{ name: 'HomeView' }" class="nav-link" active-class="nav-link-active">홈</RouterLink>
          <RouterLink :to="{ name: 'MovieView' }" class="nav-link" active-class="nav-link-active">영화</RouterLink>
        </div>
      </div>

      <!-- nav-right 부분의 검색 섹션 수정 -->
      <div v-if="store.token" class="nav-right">
        <!-- 검색 섹션 수정 -->
        <div class="search-section">
          <div class="search-wrapper" :class="{ 'is-focused': isSearchFocused }">
            <i class="fas fa-search search-icon"></i>
            <input type="text" v-model="searchQuery" placeholder="사용자를 검색해보세요." class="search-input" @focus="isSearchFocused = true" @blur="handleSearchBlur" />
            <!-- 검색 결과 드롭다운 -->
            <div v-if="isSearchFocused && searchResults.length > 0" class="search-results-dropdown">
              <RouterLink v-for="user in searchResults" :key="user.id" :to="{ name: 'ProfileView', params: { user_id: user.id } }" class="user-item" @mousedown.prevent>
                <img :src="store.API_URL + user.profile_img" alt="" class="user-avatar" />
                <div class="user-info">
                  <div class="user-name">{{ user.name }}</div>
                  <div class="user-email">{{ user.email }}</div>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>

        <div class="profile-section">
          <RouterLink v-if="store.currentUser" :to="{ name: 'ProfileView', params: { user_id: store.currentUser.id } }" class="profile-link">
            <img :src="store.currentUser?.profile_img" alt="프로필" class="profile-img" />
            <!-- <img :src="profile_img" alt="img" /> -->
          </RouterLink>
          <button @click="logOut" class="logout-btn">로그아웃</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import { ref, watch } from "vue";
import { debounce } from "lodash";
import axios from "axios";

const store = useCounterStore();
// console.log("현재 유저 정보", store.currentUser);

// 로그아웃
const logOut = function () {
  store.logOut();
};

// 검색 관련 상태 추가
const searchQuery = ref("");
const searchResults = ref([]);
const isSearchFocused = ref(false);

// 검색 blur 처리
const handleSearchBlur = () => {
  setTimeout(() => {
    isSearchFocused.value = false;
  }, 200);
};

// 검색 watch
watch(
  searchQuery,
  debounce((newQuery) => {
    if (!newQuery.trim()) {
      searchResults.value = [];
      return;
    }

    axios({
      method: "get",
      url: `${store.API_URL}/api/v2/search/`,
      params: { query: newQuery },
      headers: {
        Authorization: `Token ${store.token}`,
      },
    })
      .then((response) => {
        searchResults.value = response.data.filter((user) => user.id !== store.currentUser.id);
      })
      .catch((error) => {
        console.error("사용자 검색 실패:", error);
      });
  }, 300)
);
</script>

<style scoped>
.navigation {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: white;
  border-bottom: 1px solid #e6e6e6;
  z-index: 1000;
  height: 64px;
  display: flex;
  align-items: center;
}

.nav-container {
  width: 100%;
  max-width: 1300px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.site-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: rgb(71, 71, 71);
  text-decoration: none;
  letter-spacing: -0.5px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  text-decoration: none;
  color: rgb(130, 130, 130);
  font-size: 0.95rem;
  font-weight: 400;
  padding: 8px 4px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: rgb(71, 71, 71);
}

/* 활성 상태의 네비게이션 링크 스타일 */
.nav-link-active {
  color: rgb(71, 71, 71);
  font-weight: 600;
}

.profile-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-link {
  display: flex;
  align-items: center;
}

.profile-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.logout-btn {
  /* height: 32px; */
  background-color: transparent;
  color: rgb(71, 71, 71);
  font-size: 0.95rem;
  font-weight: 500;
  padding: 7px 10px;
  cursor: pointer;
  transition: color 0.2s ease;
  border: 1px solid #828282;
  border-radius: 6px;
  color: #000;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background-color: #eaeaea;
}

/* 검색 관련 스타일 */
.search-section {
  position: relative;
  width: 300px;
  margin: 0 8px;
}

.search-wrapper {
  position: relative;
  width: 100%;
  background: #f5f5f7;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.search-wrapper.is-focused {
  background: white;
  box-shadow: 0 0 0 2px #000000;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #74747b;
  font-size: 0.9rem;
}

.search-input {
  width: 100%;
  height: 38px;
  padding: 0 16px 0 36px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  background: transparent;
  color: #000000;
}

.search-input::placeholder {
  color: #74747b;
}

.search-input:focus {
  outline: none;
}

.search-results-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: white;
  border-radius: 6px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(0, 0, 0, 0.15);
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  text-decoration: none;
  color: inherit;
  transition: background-color 0.2s;
}

.user-item:hover {
  background-color: #f5f5f7;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 12px;
}

.user-info {
  flex: 1;
  overflow: hidden;
}

.user-name {
  font-size: 0.95rem;
  font-weight: 500;
  color: #000000;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 0.85rem;
  color: #74747b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .search-section {
    width: 200px;
  }
}
</style>
