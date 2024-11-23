<template>
  <div class="app-container">
    <AppNavBar v-if="!$route.meta.hideNavbar" />
    <main :class="{ 'main-content': isPaddingPage }">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import AppNavBar from "./components/common/AppNavBar.vue";
import { RouterView, useRoute } from "vue-router";
import { computed } from "vue";

const route = useRoute();
const isPaddingPage = computed(() => route.path !== "/" && route.path !== "/signup");
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.main-content {
  padding-top: 64px;
}
</style>
