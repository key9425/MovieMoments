<template>
  <AppNavBar />
  <RouterView />
</template>

<script setup>
import { RouterView } from "vue-router";
import AppNavBar from "./components/common/AppNavBar.vue";
</script>

<style scoped></style>
