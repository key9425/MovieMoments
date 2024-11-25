<template>
  <div class="article-container">
    <!-- 게시글 작성 폼 -->
    <div class="article-form">
      <form @submit.prevent="submitArticle">
        <textarea v-model="content" placeholder="게시글을 작성해주세요..." class="article-textarea"></textarea>
        <div class="char-count">{{ content.length }}/2000</div>

        <!-- 이미지 업로드 영역 -->
        <div class="image-upload-area">
          <label for="image-upload" class="image-upload-label">
            <div class="upload-icon">+</div>
            <span>사진 추가</span>
          </label>
          <input type="file" id="image-upload" multiple accept="image/*" @change="handleImageUpload" class="hidden" />

          <!-- 미리보기 이미지 -->
          <div class="preview-images" v-if="images.length">
            <div v-for="(image, index) in imagePreviews" :key="index" class="preview-image-container">
              <img :src="image" class="preview-image" />
              <button @click.prevent="removeImage(index)" class="remove-image">×</button>
            </div>
          </div>
        </div>

        <button type="submit" class="add-article-btn" :disabled="isSubmitting || !content.trim()">등록</button>
      </form>
    </div>

    <!-- 게시글 목록 -->
    <div class="articles-list">
      <div v-for="article in articles" :key="article.id" class="article-card">
        <!-- 게시글 헤더 -->
        <div class="article-header">
          <div class="user-info">
            <img :src="store.API_URL + article.user.profile_img" alt="User avatar" class="user-avatar" />
            <span class="username">{{ article.user.name }}</span>
          </div>
          <div class="article-actions">
            <span class="article-date">{{ formatDate(article.created_at) }}</span>
            <!-- 수정/삭제 메뉴 -->
            <div v-if="article.user.id === store.currentUser.id" class="article-menu">
              <button @click="toggleMenu(article.id)" class="menu-button">
                <i class="fas fa-ellipsis-v"></i>
              </button>
              <div v-if="activeMenu === article.id" class="menu-dropdown">
                <button @click="editArticle(article)" class="menu-item">
                  <i class="fas fa-edit"></i>
                  수정
                </button>
                <button @click="deleteArticle(article.id)" class="menu-item">
                  <i class="fas fa-trash"></i>
                  삭제
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 수정 모드 -->
        <div v-if="editingId === article.id" class="edit-form">
          <textarea v-model="editingContent" class="article-textarea"></textarea>
          <!-- 이미지 수정 영역 -->
          <div class="image-upload-area">
            <label for="edit-image-upload" class="image-upload-label">
              <div class="upload-icon">+</div>
              <span>사진 추가</span>
            </label>
            <input type="file" id="edit-image-upload" multiple accept="image/*" @change="handleEditImageUpload" class="hidden" />

            <!-- 이미지 미리보기 -->
            <div class="preview-images" v-if="editingImagePreviews.length">
              <div v-for="(image, index) in editingImagePreviews" :key="index" class="preview-image-container">
                <img :src="image" class="preview-image" />
                <button @click.prevent="removeEditImage(index)" class="remove-image">×</button>
              </div>
            </div>
          </div>

          <!-- 수정 버튼 -->
          <div class="edit-buttons">
            <button @click="updateArticle" class="save-btn">저장</button>
            <button @click="cancelEdit" class="cancel-btn">취소</button>
          </div>
        </div>

        <!-- 일반 모드 -->
        <template v-else>
          <p class="article-content">{{ article.content }}</p>
          <!-- 이미지 그리드 -->
          <div v-if="article.images.length" class="image-grid">
            <template v-if="article.images.length <= 5">
              <div v-for="(image, index) in article.images" :key="index" class="grid-image-wrapper">
                <img :src="store.API_URL + image.image" @click="showLightbox(article.images, index)" class="grid-image" />
              </div>
            </template>
            <template v-else>
              <div v-for="(image, index) in article.images.slice(0, 4)" :key="index" class="grid-image-wrapper">
                <img :src="store.API_URL + image.image" @click="showLightbox(article.images, index)" class="grid-image" />
              </div>
              <div class="grid-image-wrapper more-images" @click="showLightbox(article.images, 4)">
                <img :src="store.API_URL + article.images[4].image" class="grid-image background-image" />
                <div class="more-overlay">
                  <span>+{{ article.images.length - 4 }}</span>
                </div>
              </div>
            </template>
          </div>
        </template>
      </div>
    </div>

    <!-- Lightbox -->
    <vue-easy-lightbox :visible="visible" :imgs="imgs" :index="index" @hide="handleHide"></vue-easy-lightbox>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";
const props = defineProps({
  currentTab: {
    type: String,
    required: true, // 이 prop은 반드시 전달되어야 함
  }
});

const route = useRoute();
const store = useCounterStore();

// 기본 상태 관리
const articles = ref([]);
const content = ref("");
const images = ref([]);
const imagePreviews = ref([]);
const isSubmitting = ref(false);
const activeMenu = ref(null);
const editingId = ref(null);
const editingContent = ref("");
const editingImages = ref([]);
const editingImagePreviews = ref([]);
const showModal = ref(false);
const modalImages = ref([]);
const currentImageIndex = ref(0);
const removedImageIds = ref([]); // 삭제된 이미지 id 저장


// 게시글 조회
const getArticles = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/articles/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response.data)
      articles.value = response.data
    })
    .catch((error) => {
      console.error("게시글 조회 실패:", error);
    });
};

// 이미지 처리
const handleImageUpload = (event) => {
  const files = Array.from(event.target.files);
  images.value = [...images.value, ...files];
  // 기존 미리보기에 새로운 미리보기 추가
  imagePreviews.value = [
    ...imagePreviews.value,
    ...files.map(file => URL.createObjectURL(file))
  ];
};

const handleEditImageUpload = (event) => {
  const files = Array.from(event.target.files);
  editingImages.value = [
    ...editingImages.value,
    ...files.map((file) => ({
      file,
      isExisting: false,
    })),
  ];
  // 미리보기 추가
  editingImagePreviews.value = [
    ...editingImagePreviews.value,
    ...files.map(file => URL.createObjectURL(file))
  ];
};

const removeImage = (index) => {
  URL.revokeObjectURL(imagePreviews.value[index]);
  images.value = images.value.filter((_, i) => i !== index);
  imagePreviews.value = imagePreviews.value.filter((_, i) => i !== index);
};

const removeEditImage = (index) => {
  const removedImage = editingImages.value[index];
  if (removedImage.isExisting) {
    removedImageIds.value.push(removedImage.id);
  }
  URL.revokeObjectURL(editingImagePreviews.value[index]);
  editingImages.value = editingImages.value.filter((_, i) => i !== index);
  editingImagePreviews.value = editingImagePreviews.value.filter((_, i) => i !== index);
};

// 게시글 CRUD
const submitArticle = () => {
  if (!content.value.trim() || isSubmitting.value) return;

  isSubmitting.value = true;
  const formData = new FormData();
  formData.append("content", content.value);

  images.value.forEach((file) => {
    formData.append("images", file);
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
      content.value = '';
      images.value = [];
      imagePreviews.value = [];
      isSubmitting.value = false;
    })
    .catch((error) => {
      console.error("게시글 생성 실패:", error);
      alert("게시글 등록에 실패했습니다.");
    })
    .finally(() => {
      isSubmitting.value = false;
    });
};

const editArticle = (article) => {
  editingId.value = article.id;
  editingContent.value = article.content;
  editingImages.value = article.images.map((img) => ({
    id: img.id,
    image: img.image,
    isExisting: true,
  }));
  editingImagePreviews.value = article.images.map((img) => store.API_URL + img.image);
  activeMenu.value = null;
  removedImageIds.value = [];
};

const updateArticle = () => {
  if (!editingContent.value.trim()) return;

  const formData = new FormData();
  formData.append("content", editingContent.value);
  
  // 새로운 이미지만 필터링하여 추가
  const newImages = editingImages.value.filter(image => !image.isExisting);
  newImages.forEach(image => {
    formData.append("images", image.file);
  });

  // 삭제할 이미지 ID 추가
  removedImageIds.value.forEach(id => {
    formData.append("removed_image_ids", id);
  });

  axios({
    method: "put",
    url: `${store.API_URL}/api/v1/group/movie/article/${editingId.value}/`,
    headers: {
      Authorization: `Token ${store.token}`,
      "Content-Type": "multipart/form-data",
    },
    data: formData,
  })
    .then((response) => {
      console.log(response)
      const index = articles.value.findIndex((a) => a.id === editingId.value);
      if (index !== -1) {
        articles.value[index] = response.data;
      }
      editingId.value = null;
      editingContent.value = '';
      editingImages.value = [];
      editingImagePreviews.value = [];
    })
    .catch((error) => {
      console.error("게시글 수정 실패:", error);
      alert("게시글 수정에 실패했습니다.");
    });
};

const deleteArticle = (articleId) => {
  if (!confirm("정말 이 게시글을 삭제하시겠습니까?")) return;

  axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/group/movie/article/${articleId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      articles.value = articles.value.filter((article) => article.id !== articleId);
    })
    .catch((error) => {
      console.error("게시글 삭제 실패:", error);
      alert("게시글 삭제에 실패했습니다.");
    });
};

// 유틸리티 함수
const formatDate = (date) => {
  return new Date(date).toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const toggleMenu = (articleId) => {
  activeMenu.value = activeMenu.value === articleId ? null : articleId;
};

const cancelEdit = () => {
  editingId.value = null;
  editingContent.value = "";
  editingImages.value = [];
  editingImagePreviews.value = [];
};

const resetForm = () => {
  content.value = "";
  images.value.forEach((_, index) => {
    URL.revokeObjectURL(imagePreviews.value[index]);
  });
  images.value = [];
  imagePreviews.value = [];
};

// 라이프사이클 훅
onMounted(() => {
  getArticles();
});

onUnmounted(() => {
  // Object URL 정리
  imagePreviews.value.forEach((url) => URL.revokeObjectURL(url));
  editingImagePreviews.value.forEach((url) => URL.revokeObjectURL(url));
});
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

.edit-form {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  margin-top: 12px;
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

.article-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.article-date {
  color: #666;
  font-size: 0.9em;
}

.article-menu {
  position: relative;
}

.menu-button {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #666;
}

.menu-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  background: none;
  cursor: pointer;
  white-space: nowrap;
  color: #333;
}

.menu-item:hover {
  background: #f8f9fa;
}

.menu-item i {
  font-size: 0.9rem;
}

.article-content {
  margin-bottom: 12px;
  line-height: 1.5;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.grid-image-wrapper {
  position: relative;
  padding-bottom: 100%;
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

.edit-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.save-btn,
.cancel-btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.save-btn {
  background: #666;
  color: white;
}

.cancel-btn {
  background: #f8f9fa;
  color: #666;
  border: 1px solid #e1e1e1;
}

.save-btn:hover {
  background: #555;
}

.cancel-btn:hover {
  background: #f1f3f5;
}

@media (max-width: 768px) {
  .image-grid {
    grid-template-columns: 1fr;
  }

  .grid-image-wrapper {
    padding-bottom: 100%;
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
