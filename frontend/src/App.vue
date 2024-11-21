<template>
  <div class="app-container">
    <AppNavBar />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import AppNavBar from "./components/common/AppNavBar.vue";
import { RouterView } from "vue-router";
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore();
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.main-content {
  padding-top: 100px; /* Navbar 높이만큼 상단 여백 추가 */
}
</style>
