<template>
  <div v-if="currentTab === 'article'" class="article-container">
    <!-- 게시글 작성 폼 -->
    <div class="article-form">
      <form @submit.prevent="submitArticle">
        <textarea v-model="newArticle.content" placeholder="게시글을 작성해주세요..." class="article-textarea"></textarea>
        <div class="char-count">{{ newArticle.content.length }}/2000</div>

        <!-- 이미지 업로드 영역 -->
        <div class="image-upload-area">
          <label for="image-upload" class="image-upload-label">
            <div class="upload-icon">+</div>
            <span>사진 추가</span>
          </label>
          <input type="file" id="image-upload" multiple accept="image/*" @change="handleImageUpload" class="hidden" />

          <!-- 미리보기 이미지 -->
          <div class="preview-images" v-if="newArticle.images.length">
            <div v-for="(image, index) in newArticle.images" :key="index" class="preview-image-container">
              <img :src="image.url" class="preview-image" />
              <button @click="removeImage(index)" class="remove-image">×</button>
            </div>
          </div>
        </div>

        <button type="submit" class="add-article-btn" :disabled="isSubmitting || (!newArticle.content.trim() && !newArticle.images.length)">등록</button>

        <!-- <button @click="submitArticle" class="submit-button">게시하기</button> -->
      </form>
    </div>

    <!-- 게시글 목록 -->
    <div class="articles-list">
      <div v-for="article in articles" :key="article.id" class="article-card">
        <div class="article-header">
          <div class="user-info">
            <img :src="article.userAvatar" alt="User avatar" class="user-avatar" />
            <span class="username">{{ article.username }}</span>
          </div>
          <span class="article-date">{{ formatDate(article.createdAt) }}</span>
        </div>

        <p class="article-content">{{ article.content }}</p>

        <!-- 이미지 그리드 -->
        <div v-if="article.images.length" class="image-grid">
          <template v-if="article.images.length <= 2">
            <div v-for="(image, index) in article.images" :key="index" class="grid-image-wrapper">
              <img :src="image.url" @click="openImageModal(article.images, index)" class="grid-image" />
            </div>
          </template>

          <template v-else>
            <div v-for="(image, index) in article.images.slice(0, 2)" :key="index" class="grid-image-wrapper">
              <img :src="image.url" @click="openImageModal(article.images, index)" class="grid-image" />
            </div>
            <div class="grid-image-wrapper more-images" @click="openImageModal(article.images, 2)">
              <img :src="article.images[2].url" class="grid-image background-image" />
              <div class="more-overlay">
                <span>+{{ article.images.length - 2 }}</span>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- 이미지 모달 -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">×</button>
        <div class="modal-images">
          <img :src="modalImages[currentImageIndex].url" class="modal-image" />
        </div>
        <div class="modal-controls">
          <button @click="previousImage" :disabled="currentImageIndex === 0" class="modal-nav-button">←</button>
          <span class="image-counter">{{ currentImageIndex + 1 }} / {{ modalImages.length }}</span>
          <button @click="nextImage" :disabled="currentImageIndex === modalImages.length - 1" class="modal-nav-button">→</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from "vue";

const props = defineProps({
  currentTab: {
    type: String,
    required: true,
  },
});

// 상태 관리
const newArticle = ref({
  content: "",
  images: [],
});

const articles = ref([
  {
    id: 1,
    username: "사용자1",
    userAvatar: "/api/placeholder/40/40",
    content: "오늘 영화 너무 재미있었어요!",
    createdAt: new Date(),
    images: [{ url: "/api/placeholder/800/600" }, { url: "/api/placeholder/800/600" }, { url: "/api/placeholder/800/600" }, { url: "/api/placeholder/800/600" }],
  },
]);

const showModal = ref(false);
const modalImages = ref([]);
const currentImageIndex = ref(0);

// 이미지 업로드 처리
const handleImageUpload = (event) => {
  const files = Array.from(event.target.files);

  files.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      newArticle.value.images.push({
        url: e.target.result,
        file: file,
      });
    };
    reader.readAsDataURL(file);
  });
};

// 이미지 제거
const removeImage = (index) => {
  newArticle.value.images.splice(index, 1);
};

// 게시글 제출
const submitArticle = () => {
  if (!newArticle.value.content.trim() && !newArticle.value.images.length) return;

  articles.value.unshift({
    id: Date.now(),
    username: "사용자",
    userAvatar: "/api/placeholder/40/40",
    content: newArticle.value.content,
    createdAt: new Date(),
    images: [...newArticle.value.images],
  });

  // 폼 초기화
  newArticle.value = {
    content: "",
    images: [],
  };
};

// 모달 컨트롤
const openImageModal = (images, startIndex) => {
  modalImages.value = images;
  currentImageIndex.value = startIndex;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const previousImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--;
  }
};

const nextImage = () => {
  if (currentImageIndex.value < modalImages.value.length - 1) {
    currentImageIndex.value++;
  }
};

// 날짜 포맷
const formatDate = (date) => {
  return new Date(date).toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};
</script>

<style scoped>
.article-container {
  margin: 32px auto 0;
}

.article-form {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.char-count {
  text-align: right;
  font-size: 0.8rem;
  color: #666;
  padding: 0 0.5rem;
}

.article-textarea {
  width: 100%;
  min-height: 100px;
  padding: 12px;
  border: 1px solid #e1e1e1;
  border-radius: 4px;
  resize: vertical;
  margin-bottom: 12px;
}

.article-textarea:focus {
  outline: none;
  border-color: #666;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1);
}

.image-upload-area {
  margin-bottom: 12px;
}

.image-upload-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px dashed #e1e1e1;
  border-radius: 4px;
  cursor: pointer;
}

.upload-icon {
  font-size: 20px;
}

.hidden {
  display: none;
}

.preview-images {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.preview-image-container {
  position: relative;
  width: 100px;
  height: 100px;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.remove-image {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  cursor: pointer;
}

.add-article-btn {
  width: 100%;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  border: none;
  background: #666;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-article-btn:hover:not(:disabled) {
  background: #555;
  transform: translateY(-1px);
}

.add-article-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

/* .submit-button {
  width: 100%;
  padding: 12px;
  background: #3a3a3a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
} */

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.username {
  font-weight: 500;
}

.article-date {
  color: #666;
  font-size: 0.9em;
}

.article-content {
  margin-bottom: 12px;
  line-height: 1.5;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
}
.grid-image-wrapper {
  position: relative;
  padding-bottom: 100%; /* 정사각형 비율 생성 */
  overflow: hidden;
}

.grid-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
}

.more-images {
  position: relative;
  cursor: pointer;
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.7);
}

.more-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 24px;
  font-weight: bold;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
}

.modal-images {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.modal-image {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  display: block;
  margin: 0 auto;
}

.modal-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  color: white;
  width: 100%;
}

.modal-nav-button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
}

.modal-nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.image-counter {
  font-size: 14px;
}

@media (max-width: 768px) {
  .image-grid {
    grid-template-columns: 1fr;
  }
  .grid-image-wrapper {
    padding-bottom: 100%; /* 모바일에서도 정사각형 유지 */
  }

  .grid-image {
    height: 250px;
  }

  .modal-content {
    width: 100%;
    padding: 0 20px;
  }

  .modal-image {
    max-height: 70vh;
  }
}
</style>
