<template>
  <div>
    <h1>GroupDetail</h1>
    <button @click="goGroupMovieCreate">그룹영화생성</button>

    <div v-if="groupData">
      <img :src="'http://127.0.0.1:8000' + groupData.group_img" alt="그룹대표이미지" width="200px" />
      <h2>그룹명 : {{ groupData.group_name }}</h2>
      <p>그룹설명 : {{ groupData.description }}</p>

      <div v-for="member in groupData.include_members" :key="member.id">
        <img :src="'http://127.0.0.1:8000' + member.profile_img" alt="member.name" width="30px" />
        <h4>이름 : {{ member.name }}</h4>
        <p>이메일 : {{ member.email }}</p>
      </div>

      <!-- 그룹 영화 카드  -->
      <div class="groups-grid">
        <!-- <MovieWatchCard v-for="group_movie in groupData.watched_movies" :key="group_movie.id" :watched_movie="group_movie" class="group-card" /> -->
        <MovieWatchCard v-for="group_movie in groupData.watched_movies" :key="group_movie.id" :watchedMovie="group_movie" :groupId="route.params.group_id" class="group-card" />
      </div>
    </div>
  </div>
</template>

<script setup>
import MovieWatchCard from "@/components/MovieWatchCard.vue";
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute, useRouter, RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const router = useRouter();
const store = useCounterStore();
const API_URL = store.API_URL;

const goGroupMovieCreate = () => {
  router.push({ name: "GroupMovieCreateView" });
};

// 그룹 가져오기
const route = useRoute();

// 그룹 상세 데이터 가져오기
const groupData = ref(null);
const getGroupData = () => {
  const groupID = route.params.group_id;
  axios({
    method: "get",
    url: `${API_URL}/api/v1/groups/${groupID}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("response = ", response);
      // console.log("Group data structure:", JSON.stringify(response.data, null, 2));
      groupData.value = response.data;
    })
    .catch((error) => {
      console.error("그룹 상세 데이터 가져오기 실패:", error);
    });
};

onMounted(() => {
  getGroupData();
});
</script>

<style scoped>
.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}
</style>
