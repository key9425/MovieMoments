<template>
  <div>
    <nav>
      <RouterLink :to="{ name: 'HomeView'}">Home</RouterLink>
    </nav>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
</script>

<style scoped>

</style>