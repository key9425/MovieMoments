<template>
  <nav>
    <img src="../../assets/test-logo.PNG" alt="test-logo-img" width="100" />
    <RouterLink :to="{ name: 'HomeView' }">홈</RouterLink>
    |
    <RouterLink :to="{ name: 'MovieView' }">영화</RouterLink>
    |
    <!-- 사용자 프로필 이미지로 사용 (지금은 임의로) -->
    <img src="../../assets/test-profile.png" alt="profile-img" width="50" />
    |
    <RouterLink :to="{ name: 'ProfileView' }">Profile</RouterLink>
    |
    <div v-if="store.token">
      <button @click="logOut">로그아웃</button>
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

<style scoped></style>
