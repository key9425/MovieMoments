<template>
  <nav>
    <img src="../../assets/test-logo.PNG" alt="test-logo-img" width="100" />
    <RouterLink :to="{ name: 'HomeView' }">홈</RouterLink>
    |
    <RouterLink :to="{ name: 'MovieView' }">영화</RouterLink>
    |
    <!-- 사용자 프로필 이미지로 사용 (지금은 임의로) -->
    <img src="../../assets/test-profile.png" alt="profile-img" width="50" />
    <button>로그아웃</button>
  </nav>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped></style>
