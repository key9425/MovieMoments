<template>
  <div class="user-profile">
    <!-- 프로필 정보 표시 -->
    <div class="follow-info">
      <p>{{ name }}</p>
      <p>{{ username }}</p>
      <p>{{ email }}</p>
      <img :src="profile_img" alt="프로필 이미지" />

      <p>팔로워: {{ followers_count }}</p>
      <p>팔로잉: {{ followings_count }}</p>

      <!-- 자신의 프로필이 아닐 경우에만 팔로우 버튼 표시 -->
      <!-- <button 
        v-if="user.username !== currentUser.username"
        @click="handleFollow"
      >
        {{ isFollowing ? '언팔로우' : '팔로우' }}
      </button> -->
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { ref, onMounted } from "vue";

const name = ref(null);
const username = ref(null);
const email = ref(null);
const profile_img = ref(null);
const followers_count = ref(null);
const followings_count = ref(null);

const store = useCounterStore();

onMounted(() => {
  console.log(store.token);
  axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v2/${2}/profile/`,
    headers: {
      Authorization: `Token ${'a25cacb324cd2afce925d8883bf02bad56ce5057'}`,
    },
  })
    .then((res) => {
      console.log(res.data);
      name.value = res.data.name;
      username.value = res.data.username;
      email.value = res.data.email;
      profile_img.value = `${store.API_URL}${res.data.profile_img}`;
      followers_count.value = res.data.followers_count;
      followings_count.value = res.data.followings_count;
    })
    .catch((err) => {
      console.log(err);
    });
});
</script>

<style scoped></style>

