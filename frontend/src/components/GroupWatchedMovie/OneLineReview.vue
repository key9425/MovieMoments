<template>
  <section v-if="currentTab === 'reviews'" class="reviews-section">
    <!-- 리뷰 목록 -->
    <div class="review-card" v-for="review in reviews" :key="review.id">
      <div class="review-header">
        <div class="user-info">
          <img :src="review.userProfile" :alt="review.userName" class="user-avatar" />
          <span class="user-name">{{ review.userName }}</span>
        </div>
        <span class="review-date">{{ review.date }}</span>
      </div>
      <p class="review-text">{{ review.content }}</p>
    </div>

    <!-- 리뷰 작성 폼 -->
    <div class="review-input-form">
      <form @submit.prevent="submitReview" class="input-group">
        <input v-model="newReview" type="text" placeholder="영화에 대한 한줄평을 작성해주세요." class="review-input" :maxlength="200" required />
        <button type="submit" class="add-review-btn" :disabled="isSubmitting || !newReview.trim()">등록</button>
      </form>
      <div class="char-count">{{ newReview.length }}/200</div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { useRoute } from "vue-router";

const props = defineProps(["currentTab"]);
const store = useCounterStore();
const route = useRoute();

// 기존에 작성한 리뷰데이터 받아오기
const reviews = ref([]);
const getReview = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/groups/${route.params.group_movie_id}/reviews/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response.data);
      reviews.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
};

// const reviews = ref([
//   {
//     id: 1,
//     userName: "민지",
//     userProfile: "/api/placeholder/40/40",
//     content: "시간 가는 줄 몰랐어요! 플롯이 정말 탄탄해요.",
//     date: "2024.03.15",
//   },
// ]);

const newReview = ref("");
const isSubmitting = ref(false);

// 리뷰 제출 요청
const submitReview = async () => {
  if (!newReview.value.trim()) return;

  try {
    isSubmitting.value = true;

    const review = {
      id: Date.now(),
      userName: "현재 사용자",
      userProfile: "/api/placeholder/40/40",
      content: newReview.value,
      date: new Date().toLocaleDateString("ko-KR"),
    };

    reviews.value.push(review); // 새 리뷰를 목록 끝에 추가
    newReview.value = "";
  } catch (error) {
    console.error("리뷰 제출 실패:", error);
  } finally {
    isSubmitting.value = false;
  }
};
onMounted(() => {
  getReview();
});
</script>

<style scoped>
/* 리뷰 섹션 스타일 */
.reviews-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.review-card {
  background: #f8f9fa;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  padding: 1.5rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-name {
  font-weight: 500;
  color: #333;
}

.review-date {
  color: rgba(0, 0, 0, 0.5);
  font-size: 0.9rem;
}

/* 입력 폼 스타일 */
.review-input-form {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
}

.input-group {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0.5rem;
}

.review-input {
  flex-grow: 1;
  padding: 0.8rem;
  border-radius: 8px;
  border: 1px solid #e1e1e1;
  background: #ffffff;
  color: #333333;
  font-size: 0.95rem;
}

.review-input:focus {
  outline: none;
  border-color: #3a3a3a;
  box-shadow: 0 0 0 2px rgba(41, 128, 185, 0.1);
}

.add-review-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  border: none;
  background: #3a3a3a;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.add-review-btn:hover:not(:disabled) {
  background: #2471a3;
  transform: translateY(-1px);
}

.add-review-btn:active {
  transform: translateY(0);
}

.add-review-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.char-count {
  text-align: right;
  font-size: 0.8rem;
  color: #666;
  padding: 0 0.5rem;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .input-group {
    flex-direction: column;
    gap: 0.5rem;
  }

  .add-review-btn {
    width: 100%;
  }

  .review-input-form {
    padding: 1rem;
  }
}
</style>
