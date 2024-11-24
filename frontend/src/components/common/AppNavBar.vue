<template>
  <nav class="navigation">
    <div class="nav-container">
      <div class="nav-left">
        <RouterLink :to="{ name: 'HomeView' }" class="site-title">영화처럼, 순간처럼</RouterLink>
      </div>

      <div v-if="store.token" class="nav-right">
        <div class="nav-links">
          <RouterLink :to="{ name: 'HomeView' }" class="nav-link" active-class="nav-link-active">홈</RouterLink>
          <RouterLink :to="{ name: 'MovieView' }" class="nav-link" active-class="nav-link-active">영화</RouterLink>
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

const store = useCounterStore();
// console.log("현재 유저 정보", store.currentUser);

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
  gap: 32px;
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
  gap: 16px;
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
</style>
