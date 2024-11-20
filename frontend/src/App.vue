<template>
  <!-- <AppNavBar /> -->
  <RouterLink :to="{ name: 'SignUpForm' }">SignUpForm</RouterLink> |
  <RouterLink :to="{ name: 'ProfileView' }">Profile</RouterLink>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
// import AppNavBar from "./components/common/AppNavBar.vue";
</script>

<style scoped></style>
