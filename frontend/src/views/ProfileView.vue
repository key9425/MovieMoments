<template>
  <div class="user-profile">
    <div class="follow-info">
      <p>{{ name }}</p>
      <p>{{ username }}</p>
      <p>{{ email }}</p>
      <img :src="profile_img" alt="프로필 이미지" />

      <p>팔로워: {{ followers_count }}</p>
      <p>팔로잉: {{ followings_count }}</p>

      <!-- 자신의 프로필이 아닐 경우에만 팔로우 버튼 표시 -->
      <button v-if="id !== store.currentUser.id" @click="follow">
        {{ is_following ? '언팔로우' : '팔로우' }}
      </button>

      <button v-if="id === store.currentUser.id" @click="deleteAccount">회원탈퇴</button>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { useCounterStore}  from "@/stores/counter";
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const id = ref(null);
const name = ref(null);
const username = ref(null);
const email = ref(null);
const profile_img = ref(null);
const followers_count = ref(null);
const followings_count = ref(null);
const is_following = ref(null);

const store = useCounterStore();
const route = useRoute();

// 서버 응답에 count 데이터를 포함
//실제 DB 상태와 불일치가 발생할 수 있음
// 다른 사용자의 동시 팔로우/언팔로우를 반영할 수 없음
const follow = function () {
  axios({
    method: "post",
    url: `http://127.0.0.1:8000/api/v2/${route.params.user_id}/follow/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
  .then((res) => {
      console.log(res.data);
      followers_count.value = res.data.followers_count;
      followings_count.value = res.data.followings_count;
      is_following.value = res.data.is_following; 
    })
    .catch((err) => {
      console.log(err);
    });
}

const deleteAccount = function () {
  store.deleteAccount()
}

onMounted(() => {
  axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v2/${route.params.user_id}/profile/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      console.log(res.data);
      id.value = res.data.id;
      name.value = res.data.name;
      username.value = res.data.username;
      email.value = res.data.email;
      profile_img.value = res.data.profile_img;
      followers_count.value = res.data.followers_count;
      followings_count.value = res.data.followings_count;
      is_following.value = res.data.is_following; 
    })
    .catch((err) => {
      console.log(err);
    });
});
</script>

<style scoped>
</style>