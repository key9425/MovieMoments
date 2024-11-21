<template>
  <AppNavBar />
  <RouterView />
</template>

<script setup>
import AppNavBar from "./components/common/AppNavBar.vue";
import { RouterView } from "vue-router";
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore();
</script>

<style scoped></style>
