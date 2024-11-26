<template>
  <section class="reviews-section">
    <!-- 리뷰 작성 폼 -->
    <div class="review-form-card">
      <h3 class="form-title">한줄평 작성</h3>
      <form @submit.prevent="submitReview" class="review-form">
        <div class="input-wrapper">
          <input v-model="newReview" type="text" placeholder="영화에 대한 생각을 한 줄로 남겨주세요." class="review-input" :maxlength="200" required />
          <div class="char-count" :class="{ 'near-limit': newReview.length > 180 }">{{ newReview.length }}/200</div>
        </div>
        <button type="submit" class="submit-btn" :disabled="isSubmitting || !newReview.trim()">
          <i class="fas fa-paper-plane"></i>
          등록
        </button>
      </form>
    </div>

    <!-- 리뷰 목록 -->
    <div class="reviews-container">
      <div v-if="!reviews.length" class="empty-state">
        <i class="fas fa-comments empty-icon"></i>
        <p>아직 작성된 한줄평이 없습니다. 첫 번째 한줄평을 남겨보세요!</p>
      </div>

      <div v-else v-for="review in sortedReviews" :key="review.id" class="review-card" :class="{ 'fade-enter': review.isNew }">
        <div class="review-header">
          <div class="user-info">
            <img :src="store.API_URL + review.user.profile_img" :alt="review.user.name" class="user-avatar" loading="lazy" />
            <div class="user-details">
              <span class="user-name">{{ review.user.name }}</span>
              <span class="review-date">{{ formatDate(review.created_at) }}</span>
            </div>
          </div>

          <button v-if="review.user.id === store.currentUser?.id" @click="deleteReview(review.id)" class="delete-btn" aria-label="한줄평 삭제">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>

        <div class="review-content">
          <p>{{ review.review }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute } from "vue-router";
import axios from "axios";

const store = useCounterStore();
const route = useRoute();

// 상태 관리
const reviews = ref([]);
const newReview = ref("");
const isSubmitting = ref(false);

// 정렬된 리뷰 목록 (최신순)
const sortedReviews = computed(() => {
  return [...reviews.value].sort((a, b) => {
    return new Date(b.created_at) - new Date(a.created_at);
  });
});

// 리뷰 조회
const getReviews = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    if (response.data.review) {
      reviews.value = response.data.review;
    }
  } catch (error) {
    console.error("한줄평 조회 실패:", error);
  }
};

// 리뷰 작성
const submitReview = async () => {
  if (!newReview.value.trim() || isSubmitting.value) return;

  isSubmitting.value = true;

  try {
    const response = await axios({
      method: "post",
      url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/review/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
      data: {
        review: newReview.value,
      },
    });

    // 새로운 리뷰에 애니메이션 플래그 추가
    const newReviewData = { ...response.data, isNew: true };
    reviews.value = [newReviewData, ...reviews.value];
    newReview.value = "";

    // 애니메이션 플래그 제거
    setTimeout(() => {
      reviews.value = reviews.value.map((review) => ({
        ...review,
        isNew: false,
      }));
    }, 300);
  } catch (error) {
    console.error("한줄평 작성 실패:", error);
  } finally {
    isSubmitting.value = false;
  }
};

// 리뷰 삭제
const deleteReview = async (reviewId) => {
  if (!confirm("이 한줄평을 삭제하시겠습니까?")) return;

  try {
    await axios({
      method: "delete",
      url: `${store.API_URL}/api/v1/group/movie/review/${reviewId}/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    reviews.value = reviews.value.filter((review) => review.id !== reviewId);
  } catch (error) {
    console.error("한줄평 삭제 실패:", error);
  }
};

// 날짜 포맷팅
const formatDate = (date) => {
  return new Date(date).toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

onMounted(() => {
  getReviews();
});
</script>

<style scoped>
.reviews-section {
  padding: 1rem 0;
}

/* 폼 스타일 */
.review-form-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.review-form {
  display: flex;
  gap: 1rem;
}

.input-wrapper {
  flex: 1;
  position: relative;
}

.review-input {
  width: 100%;
  padding: 1rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  background: #f8f9fa;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.review-input:focus {
  outline: none;
  border-color: #dc3545;
  background: white;
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
}

.char-count {
  position: absolute;
  right: 1rem;
  bottom: -1.5rem;
  font-size: 0.8rem;
  color: #6c757d;
}

.char-count.near-limit {
  color: #dc3545;
}

.submit-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1.5rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  background: #c82333;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background: #e9ecef;
  cursor: not-allowed;
}

/* 리뷰 목록 스타일 */
.reviews-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: #6c757d;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.review-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  opacity: 1;
  transform: translateY(0);
}

.review-card.fade-enter {
  opacity: 0;
  transform: translateY(-20px);
}

.review-card:hover {
  transform: translateY(-2px);
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
  object-fit: cover;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: #333;
}

.review-date {
  font-size: 0.8rem;
  color: #6c757d;
}

.delete-btn {
  background: none;
  border: none;
  color: #dc3545;
  opacity: 0;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.review-card:hover .delete-btn {
  opacity: 0.7;
}

.delete-btn:hover {
  opacity: 1;
  transform: scale(1.1);
}

.review-content {
  color: #333;
  line-height: 1.6;
}

.review-content p {
  margin: 0;
}

@media (max-width: 768px) {
  .reviews-section {
    padding: 1rem;
  }

  .review-form {
    flex-direction: column;
  }

  .submit-btn {
    width: 100%;
    padding: 1rem;
  }

  .char-count {
    bottom: -2.5rem;
  }

  .delete-btn {
    opacity: 0.7;
  }

  .review-form-card {
    margin-bottom: 3rem;
  }
}
</style>
