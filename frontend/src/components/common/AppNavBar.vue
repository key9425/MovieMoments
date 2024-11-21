<template>
  <nav class="navigation">
    <div class="nav-content">
      <div class="nav-left">
        <h1 class="site-title">영화처럼, 순간처럼</h1>
      </div>
    </div>
    <div v-if="store.token" class="nav-right">
      <!-- 네비게이션 아이템 -->
      <RouterLink :to="{ name: 'HomeView' }" class="nav-link">홈</RouterLink>
      <RouterLink :to="{ name: 'MovieView' }" class="nav-link">영화</RouterLink>

      <div class="profile-button">
        <!-- 프로필 이미지를 RouterLink로 감싸서 클릭 시 프로필 페이지로 이동 -->
        <RouterLink v-if="store.currentUser" :to="{ name: 'ProfileView', params: { user_id: store.currentUser.id } }" class="profile-link">
          <img :src="store.currentUser?.profile_img || 'https://via.placeholder.com/32'" alt="프로필" class="profile-img" />
        </RouterLink>

        <!-- 로그아웃 버튼 -->
        <button class="nav-link logout-btn" @click="logOut">로그아웃</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore();

const logOut = function () {
  store.logOut();
};
</script>

<style scoped>
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
  /* max-width: 1200px; */
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.site-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ff7336; /* 반려생활 로고색 */
  letter-spacing: -0.5px;
}

.nav-right {
  display: flex;
  flex-direction: row;
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

.nav-link.logout-btn {
  padding: 0 10px;
  color: white;
  background-color: #ff8a05;
  border-radius: 5px;
}

.nav-link:hover {
  color: #454545;
  /* background-color: #ff8a05; */
}

.profile-button {
  border-radius: 4px;
  display: flex;
  gap: 12px;
}

.profile-img {
  width: 32px;
  height: 32px;
  object-fit: cover;
}
</style>
