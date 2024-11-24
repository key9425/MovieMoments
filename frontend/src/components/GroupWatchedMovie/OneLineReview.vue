<template>
  <section v-if="currentTab === 'reviews'" class="reviews-section">
    <!-- 리뷰 작성 폼 -->
    <div class="review-input-form">
      <form @submit.prevent="submitReview" class="input-group">
        <input v-model="newReview" type="text" placeholder="영화에 대한 한줄평을 작성해주세요." class="review-input" :maxlength="200" required />
        <div class="char-count">{{ newReview.length }}/200</div>
        <button type="submit" class="add-review-btn" :disabled="isSubmitting || !newReview.trim()">등록</button>
      </form>
    </div>
    <!-- 리뷰 목록 -->
    <!-- 받아오는 거 보고 변수명 바꾸기 -->
    <div class="review-card" v-for="review in reviews" :key="review.id">
      <div class="review-header">
        <div class="user-info">
          <img :src="store.API_URL + review.user.profile_img" :alt="review.name" class="user-avatar" />
          <span class="user-name">{{ review.user.name }}</span>
        </div>
        <div class="review-actions">
          <span class="review-date">{{ formatDate(review.created_at) }}</span>
          <!-- 본인이 작성한 리뷰에만 삭제 버튼 표시 -->
          <button v-if="review.user.id === store.currentUser?.id" @click="deleteReview(review.id)" class="delete-btn">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      </div>
      <p class="review-text">{{ review.review }}</p>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { useRoute } from "vue-router";

const props = defineProps({
  currentTab: {
    type: String,
    required: true,
  },
  oneLineReviewData: {
    default: () => [], // 기본값으로 빈 배열 설정
  },
});
const store = useCounterStore();
const route = useRoute();

// 기존에 작성한 리뷰데이터 받아오기
const reviews = ref([...props.oneLineReviewData]);
const getReview = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("onMount 응답 결과 : ");
      console.log("review response", response);
      reviews.value = response.data.review.sort((a, b) => {
        return new Date(b.created_at) - new Date(a.created_at);
      });
    })
    .catch((error) => {
      console.log(error);
      console.log("한줄평 받아오기 실패");
    });
};

// 새로 작성한 리뷰 제출 요청
const newReview = ref("");

const isSubmitting = ref(false);

const submitReview = () => {
  if (!newReview.value.trim()) return;

  isSubmitting.value = true;

  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/review/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: {
      review: newReview.value,
    },
  })
    .then((response) => {
      console.log("post response", response.data);
      // reviews.value.push(response.data); // 서버에서 받은 전체 리뷰 목록으로 업데이트
      reviews.value = [response.data, ...reviews.value];
      newReview.value = ""; // 입력창 초기화
      isSubmitting.value = false; // 제출 상태 해제
    })
    .catch((error) => {
      console.log(error);
      isSubmitting.value = false;
    });
};

onMounted(() => {
  getReview();
});

// 날짜 포맷
const formatDate = (date) => {
  return new Date(date).toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

// 리뷰 삭제 함수 추가
const deleteReview = (reviewId) => {
  if (!confirm("이 리뷰를 삭제하시겠습니까?")) return;

  axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/group/movie/review/${reviewId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      // 성공적으로 삭제되면 목록에서 제거
      reviews.value = reviews.value.filter((review) => review.id !== reviewId);
    })
    .catch((error) => {
      console.error("리뷰 삭제 실패:", error);
      alert("리뷰 삭제에 실패했습니다.");
    });
};
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
  flex-wrap: wrap;
  gap: 1rem;
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
  .review-actions {
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
  }

  .delete-btn {
    padding: 0.5rem 0;
  }
}

.review-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.delete-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  color: #dc3545;
  cursor: pointer;
  opacity: 0.7;
  transition: all 0.2s ease;
}

.delete-btn:hover {
  opacity: 1;
  transform: scale(1.1);
}
</style>
