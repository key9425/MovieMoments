<template>
  <div class="group-container">
    <!-- 왼쪽 사이드바: 그룹 정보 -->
    <aside class="sidebar">
      <div v-if="groupData" class="group-info">
        <img :src="'http://127.0.0.1:8000' + groupData.group_img" alt="그룹대표이미지" class="group-img" />
        <h2>{{ groupData?.group_name }}</h2>
        <p class="group-description">{{ groupData?.description }}</p>

        <!-- 멤버 목록 -->
        <div class="members-section">
          <div v-for="member in groupData.include_members" :key="member.id">
            <RouterLink :to="{ name: 'ProfileView', params: { user_id: member.id } }" class="member-item">
              <img :src="'http://127.0.0.1:8000' + member.profile_img" :alt="member.name" />
              <div class="member-info">
                <h4 class="member-name">{{ member.name }}</h4>
                <p class="member-email">{{ member.email }}</p>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
    </aside>

    <!-- 오른쪽: 영화 그리드 -->
    <main class="main-content">
      <div v-if="groupData" class="groups-grid">
        <div v-for="group_movie in groupData.watched_movies" :key="group_movie.id" class="movie-card">
          <MovieWatchCard :watchedMovie="group_movie" :groupId="route.params.group_id" />
        </div>
      </div>

      <!-- 새 영화 추가 버튼 -->
      <button @click="openModal" class="add-movie-btn">+</button>
      <!-- 모달 컴포넌트 -->
      <Transition name="modal">
        <GroupMovieCreateModal v-if="isModalOpen" @close="closeModal" @group-movie-created="onGroupMovieCreated" :id="route.params.group_id" />
      </Transition>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import MovieWatchCard from "@/components/MovieWatchCard.vue";
import GroupMovieCreateModal from "@/components/GroupMovieCreateModal.vue";
import ProfileView from "./ProfileView.vue";

export default {
  name: "GroupDetail",
  components: {
    MovieWatchCard,
    GroupMovieCreateModal,
  },
  setup() {
    const router = useRouter();
    const store = useCounterStore();
    const route = useRoute();
    const groupData = ref(null);
    const isModalOpen = ref(false); // 모달 상태 관리

    // 모달 열기
    const openModal = () => {
      isModalOpen.value = true;
      document.body.style.overflow = "hidden";
    };

    // 모달 닫기
    const closeModal = () => {
      isModalOpen.value = false;
      document.body.style.overflow = "auto";
    };

    // 영화 생성 완료 후 처리
    const onGroupMovieCreated = () => {
      closeModal();
      getGroupData(); // 그룹 데이터 새로고침
    };

    const getGroupData = () => {
      const groupID = route.params.group_id;
      axios({
        method: "get",
        url: `${store.API_URL}/api/v1/groups/${groupID}/`,
        headers: {
          Authorization: `Token ${store.token}`,
        },
      })
        .then((response) => {
          console.log("response = ", response);
          groupData.value = response.data;
        })
        .catch((error) => {
          console.error("그룹 상세 데이터 가져오기 실패:", error);
        });
    };

    onMounted(() => {
      getGroupData();
    });

    return {
      groupData,
      route,
      store,
      isModalOpen,
      openModal,
      closeModal,
      onGroupMovieCreated,
    };
  },
};
</script>

<style scoped>
.group-container {
  display: flex;
  background: #fff;
}

/* 왼쪽 사이드바 */
.sidebar {
  width: 300px;
  padding: 2rem;
  border-right: 1px solid #eee;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
  background: #fff;
}

.group-info {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.group-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.group-info h2 {
  font-size: 1.5rem;
  font-weight: bold;
}

.group-description {
  color: #666;
  line-height: 1.5;
}

.members-section {
  margin-top: 2rem;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.member-item:hover {
  background-color: #f8f9fa;
}

.member-item img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.member-info {
  display: flex;
  flex-direction: column;
}

.member-name {
  font-weight: 500;
  margin: 0;
}

.member-email {
  font-size: 0.8rem;
  color: #666;
  margin: 0;
}

/* 오른쪽 메인 영역 */
.main-content {
  flex: 1;
  margin-left: 300px;
  padding: 2rem;
  position: relative;
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

/* 새 영화 추가 버튼 */
.add-movie-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 80px; /* 50px에서 증가 */
  height: 80px; /* 50px에서 증가 */
  border-radius: 50%;
  background: white;
  border: 2px solid #ddd;
  font-size: 36px; /* 24px에서 증가 */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.add-movie-btn:hover {
  transform: translateY(-2px);
  border-color: #999;
}
/* style 섹션 맨 아래에 추가 */
/* 모달 트랜지션 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
a {
  text-decoration: none;
  color: black;
}
</style>
