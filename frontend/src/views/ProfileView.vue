<template>
  <div class="user-profile">
    <!-- 개인 정보 섹션 -->
    <div class="profile-header">
      <img :src="profile_img" alt="프로필 이미지" />
      <div class="profile-info">
        <h2>{{ name }}</h2>
        <p class="username">@{{ username }}</p>
        <p class="email">{{ email }}</p>
        <div class="stats">
          <div class="stat-item">
            <span>42</span>
            <p>글</p>
          </div>
          <div class="stat-item">
            <span>{{ followers_count }}</span>
            <p>팔로워</p>
          </div>
          <div class="stat-item">
            <span>{{ followings_count }}</span>
            <p>팔로잉</p>
          </div>
        </div>
        <button v-if="id !== store.currentUser.id" @click="follow">
          {{ is_following ? "언팔로우" : "팔로우" }}
        </button>
      </div>
    </div>

    <!-- 최근 작성한 글 -->
    <div class="profile-content">
      <div class="section-title">
        <h3>최근 작성한 글</h3>
        <span>더보기</span>
      </div>
      <div class="content-grid">
        <div class="review-card" v-for="n in 3" :key="n">
          <h4>인셉션</h4>
          <p>놀라운 연출과 흥미로운 스토리...</p>
          <span>2024.01.{{ n }}</span>
        </div>
      </div>

      <!-- 좋아요 한 영화 -->
      <div class="section-title">
        <h3>좋아요한 영화</h3>
        <span>더보기</span>
      </div>
      <div class="movie-grid">
        <div class="movie-poster" v-for="n in 4" :key="n">
          <img src="https://via.placeholder.com/150x225" alt="Movie poster" />
        </div>
      </div>
    </div>
    <div>
      <button v-if="id === store.currentUser.id" @click="deleteAccount">회원탈퇴</button>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const id = ref(null);
const name = ref(null);
const username = ref(null);
const email = ref(null);
const profile_img = ref(null);
const followers_count = ref(null);
const followings_count = ref(null);
const is_following = ref(false);

const store = useCounterStore();
const route = useRoute();

// 팔로우 요청
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
};

// 프로필 페이지 들어오면 프로필 
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

const deleteAccount = function () {
  store.deleteAccount();
};
</script>

<style scoped>
.user-profile {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  color: #1a1b25;
}

.profile-header {
  display: flex;
  gap: 3rem;
  margin-bottom: 3rem;
}

.profile-header img {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #6246ea;
}

.profile-info {
  flex-grow: 1;
}

h2 {
  font-size: 2rem;
  margin: 0;
  color: #2b2c34;
}

.username {
  color: #6246ea;
  margin: 0.5rem 0;
}

.email {
  color: #6b7280;
  margin: 0 0 1.5rem;
}

.stats {
  display: flex;
  gap: 2.5rem;
  margin-bottom: 1.5rem;
}

.stat-item {
  text-align: center;
}

.stat-item span {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2b2c34;
}

.stat-item p {
  margin: 0;
  color: #6b7280;
}

button {
  background: #6246ea;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

button:hover {
  background: #5235d1;
}

.profile-content {
  margin-top: 3rem;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-title h3 {
  color: #2b2c34;
  margin: 0;
}

.section-title span {
  color: #6246ea;
  cursor: pointer;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.review-card {
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.review-card h4 {
  margin: 0 0 0.5rem;
  color: #2b2c34;
}

.review-card p {
  margin: 0 0 1rem;
  color: #6b7280;
}

.review-card span {
  color: #9ca3af;
  font-size: 0.875rem;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.movie-poster img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  transition: transform 0.2s;
}

.movie-poster img:hover {
  transform: scale(1.05);
}
</style>
