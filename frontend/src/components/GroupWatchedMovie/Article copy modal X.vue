<template>
  <section v-if="currentTab === 'article'" class="article-section">
    <!-- 게시글 작성 폼 -->
    <div class="article-input-form">
      <form @submit.prevent="submitArticle" class="input-group">
        <textarea v-model="newArticle.content" placeholder="게시글을 작성해주세요." class="article-input" :maxlength="2000" required></textarea>
        <div class="char-count">{{ newArticle.content.length }}/2000</div>

        <!-- 이미지 업로드 영역 -->
        <div class="image-upload-area">
          <label for="image-upload" class="image-upload-label">
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
      </form>
    </div>

    <!-- 게시글 목록 -->
    <div class="article-card" v-for="article in articles" :key="article.id">
      <div class="article-header">
        <div class="user-info">
          <img :src="article.userProfile" :alt="article.username" class="user-avatar" />
          <span class="user-name">{{ article.username }}</span>
        </div>
        <span class="article-date">{{ article.created_at }}</span>
      </div>

      <p class="article-text">{{ article.content }}</p>

      <!-- 이미지 그리드 -->
      <div v-if="article.images.length" class="image-grid">
        <template v-if="article.images.length <= 2">
          <img v-for="(image, index) in article.images" :key="index" :src="image.url" @click="openImageModal(article.images, index)" class="grid-image" />
        </template>

        <template v-else>
          <img v-for="(image, index) in article.images.slice(0, 2)" :key="index" :src="image.url" @click="openImageModal(article.images, index)" class="grid-image" />
          <div class="grid-image more-images" @click="openImageModal(article.images, 2)">
            <img :src="article.images[2].url" class="background-image" />
            <div class="more-overlay">
              <span>+{{ article.images.length - 2 }}</span>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- 이미지 모달 -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">×</button>
        <div class="modal-images">
          <img :src="modalImages[currentImageIndex].url" class="modal-image" />
          <div class="modal-controls">
            <button @click="previousImage" :disabled="currentImageIndex === 0" class="modal-nav-button">←</button>
            <button @click="nextImage" :disabled="currentImageIndex === modalImages.length - 1" class="modal-nav-button">→</button>
          </div>
          <div class="image-counter">{{ currentImageIndex + 1 }} / {{ modalImages.length }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, defineProps } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import { onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";

const props = defineProps(["currentTab"]);
const store = useCounterStore();
const route = useRoute();

// 상태 관리
const newArticle = ref({
  content: "",
  images: [],
});

const articles = ref([]);
const isSubmitting = ref(false);
const showModal = ref(false);
const modalImages = ref([]);
const currentImageIndex = ref(0);

// 게시글 불러오기
const getArticles = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/articles/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      articles.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
};

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
  if ((!newArticle.value.content.trim() && !newArticle.value.images.length) || isSubmitting.value) return;

  isSubmitting.value = true;

  // FormData 생성
  const formData = new FormData();
  formData.append("content", newArticle.value.content);
  newArticle.value.images.forEach((image, index) => {
    formData.append(`images[${index}]`, image.file);
  });

  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/articles/`,
    headers: {
      Authorization: `Token ${store.token}`,
      "Content-Type": "multipart/form-data",
    },
    data: formData,
  })
    .then((response) => {
      articles.value.unshift(response.data);
      newArticle.value = {
        content: "",
        images: [],
      };
      isSubmitting.value = false;
    })
    .catch((error) => {
      console.log(error);
      isSubmitting.value = false;
    });
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

onMounted(() => {
  getArticles();
});
</script>

<style scoped>
.article-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.article-input-form {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.article-input {
  width: 100%;
  min-height: 100px;
  padding: 0.8rem;
  border-radius: 8px;
  border: 1px solid #e1e1e1;
  background: #ffffff;
  color: #333333;
  font-size: 0.95rem;
  resize: vertical;
}

.article-input:focus {
  outline: none;
  border-color: #666;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1);
}

.char-count {
  text-align: right;
  font-size: 0.8rem;
  color: #666;
  padding: 0 0.5rem;
}

.image-upload-area {
  margin: 0.5rem 0;
}

.image-upload-label {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  background: #ffffff;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.image-upload-label:hover {
  background: #f8f9fa;
  border-color: #666;
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
  border-radius: 8px;
}

.remove-image {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  cursor: pointer;
}

.add-article-btn {
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

.article-card {
  background: #f8f9fa;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  padding: 1.5rem;
}

.article-header {
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

.article-date {
  color: rgba(0, 0, 0, 0.5);
  font-size: 0.9rem;
}

.article-text {
  margin-bottom: 1rem;
  line-height: 1.6;
  color: #333;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
  margin-top: 1rem;
}

.grid-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
}

.more-images {
  position: relative;
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  filter: brightness(0.7);
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
  padding: 20px;
}

.modal-content {
  position: relative;
  width: 100%;
  max-width: 1200px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
  z-index: 1001;
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.8);
}

.modal-images {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.modal-image {
  max-width: 100%;
  max-height: calc(90vh - 100px);
  object-fit: contain;
  border-radius: 8px;
}

.modal-controls {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  pointer-events: none;
}

.modal-nav-button {
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
  pointer-events: auto;
}

.modal-nav-button:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.8);
}

.modal-nav-button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.image-counter {
  position: absolute;
  bottom: -40px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  font-size: 14px;
  background: rgba(0, 0, 0, 0.5);
  padding: 5px 10px;
  border-radius: 15px;
}

@media (max-width: 768px) {
  .article-input-form {
    padding: 1rem;
  }

  .input-group {
    gap: 0.5rem;
  }

  .add-article-btn {
    width: 100%;
  }

  .image-grid {
    grid-template-columns: 1fr;
  }

  .grid-image {
    height: 250px;
  }

  .preview-images {
    gap: 4px;
  }

  .preview-image-container {
    width: 80px;
    height: 80px;
  }

  .article-card {
    padding: 1rem;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
  }

  .user-info {
    gap: 0.5rem;
  }
  .modal-content {
    padding: 10px;
  }

  .modal-image {
    max-height: calc(100vh - 140px);
  }

  .modal-nav-button {
    width: 35px;
    height: 35px;
    font-size: 20px;
  }

  .image-counter {
    bottom: -35px;
  }
}
</style>
