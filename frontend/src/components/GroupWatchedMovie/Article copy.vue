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
      </form>
    </div>

    <!-- 게시글 목록 -->
    <div class="articles-list">
      <!-- 게시글 아이템 반복 -->
      <div v-for="article in articles" :key="article.id" class="article-card">
        <div class="article-header">
          <!-- 유저 프로필 -->
          <div class="user-info">
            <img :src="store.API_URL + article.user.profile_img" alt="User avatar" class="user-avatar" />
            <span class="username">{{ article.user.name }}</span>
          </div>
          <!-- 날짜 정보 + 더보기 버튼(for 수정, 삭제) -->
          <div class="article-actions">
            <span class="article-date">{{ formatDate(article.created_at) }}</span>
            <!-- 현재 사용자가 작성한 글인 경우에만 더보기 버튼 표시 -->
            <div v-if="article.user.id === store.currentUser.id" class="article-menu">
              <button @click="toggleMenu(article.id)" class="menu-button">
                <i class="fas fa-ellipsis-v"></i>
              </button>
              <!-- 더보기 버튼 선택된 경우에 수정 및 삭제 버튼 표시 -->
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

        <!-- 수정 모드일 때 -->
        <div v-if="editingArticle?.id === article.id">
          <textarea v-model="editingArticle.content" class="article-textarea"></textarea>
          <!-- 이미지 수정 영역 추가 -->
          <div class="image-upload-area">
            <label for="edit-image-upload" class="image-upload-label">
              <div class="upload-icon">+</div>
              <span>사진 추가</span>
            </label>
            <input type="file" id="edit-image-upload" multiple accept="image/*" @change="handleEditImageUpload" class="hidden" />

            <!-- 기존 이미지 및 새로 추가된 이미지 미리보기 -->
            <div class="preview-images" v-if="editingArticle.images.length">
              <div v-for="(image, index) in editingArticle.images" :key="index" class="preview-image-container">
                <img :src="getImageUrl(image)" class="preview-image" />
                <button @click="removeEditImage(index)" class="remove-image">×</button>
              </div>
            </div>
          </div>

          <div class="edit-buttons">
            <button @click="updateArticle(article.id)" class="save-btn">저장</button>
            <button @click="cancelEdit" class="cancel-btn">취소</button>
          </div>
        </div>
        <!-- 일반 모드일 때 -->
        <template v-else>
          <!-- 게시물 내용 -->
          <p class="article-content">{{ article.content }}</p>
          <!-- 이미지 그리드 -->
          <div v-if="article.images.length" class="image-grid">
            <template v-if="article.images.length <= 3">
              <div v-for="(image, index) in article.images" :key="index" class="grid-image-wrapper">
                <img :src="store.API_URL + image.image" @click="openImageModal(article.images, index)" class="grid-image" />
              </div>
            </template>

            <template v-else>
              <div v-for="(image, index) in article.images.slice(0, 3)" :key="index" class="grid-image-wrapper">
                <img :src="store.API_URL + image.image" @click="openImageModal(article.images, index)" class="grid-image" />
              </div>
              <div class="grid-image-wrapper more-images" @click="openImageModal(article.images, 2)">
                <img :src="store.API_URL + article.images[3].image" class="grid-image background-image" />
                <div class="more-overlay">
                  <span>+{{ article.images.length - 2 }}</span>
                </div>
              </div>
            </template>
          </div>
        </template>
      </div>
    </div>

    <!-- 이미지 모달 -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">×</button>
        <div class="modal-images">
          <img :src="store.API_URL + modalImages[currentImageIndex].image" class="modal-image" />
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
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { ref, defineProps } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const props = defineProps({
  currentTab: {
    type: String,
    required: true,
  },
  articlesData: {
    type: Array,
    default: () => [], // 기본값으로 빈 배열 설정
  },
});

const emit = defineEmits(["update:articles-images"]);

// 상태 관리
const newArticle = ref({
  content: "",
  images: [],
});
const isSubmitting = ref(false); // 제출 중 상태 관리를 위한 ref 추가
const store = useCounterStore();
const activeMenu = ref(null);
const editingArticle = ref(null);

const articles = ref(
  [...props.articlesData].sort((a, b) => {
    return new Date(b.created_at) - new Date(a.created_at);
  })
);

const showModal = ref(false);
const modalImages = ref([]);
const currentImageIndex = ref(0);

// 메뉴 토글
const toggleMenu = (articleId) => {
  activeMenu.value = activeMenu.value === articleId ? null : articleId;
};

// 수정 모드 시작
const editArticle = (article) => {
  editingArticle.value = { ...article };
  activeMenu.value = null;
};

// 수정 취소
const cancelEdit = () => {
  editingArticle.value = null;
};

// 게시글 수정
const updateArticle = (articleId) => {
  if (!editingArticle.value?.content.trim()) return;

  axios({
    method: "put",
    url: `${store.API_URL}group/movie/article/${articleId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: {
      content: editingArticle.value.content,
    },
  })
    .then((response) => {
      // 성공적으로 수정된 경우
      const updatedArticle = response.data;

      // 게시글 목록 업데이트
      const index = articles.value.findIndex((a) => a.id === articleId);
      if (index !== -1) {
        articles.value[index].content = editingArticle.value.content;
      }

      // 수정 모드 종료
      editingArticle.value = null;
      alert("게시글이 수정되었습니다.");
    })
    .catch((error) => {
      console.error("게시글 수정 실패:", error);
      alert("게시글 수정에 실패했습니다.");
    });
};

// 게시글 삭제
const deleteArticle = (articleId) => {
  if (!confirm("정말 이 게시글을 삭제하시겠습니까?")) return;

  axios({
    method: "delete",
    url: `${store.API_URL}group/movie/article/${articleId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      // 게시글 목록에서 제거
      articles.value = articles.value.filter((article) => article.id !== articleId);
      alert("게시글이 삭제되었습니다.");
    })
    .catch((error) => {
      console.error("게시글 삭제 실패:", error);
      alert("게시글 삭제에 실패했습니다.");
    });
};

// 이미지 URL 생성 함수
const getImageUrl = (image) => {
  // 새로 추가된 이미지인 경우
  if (image.url) {
    return image.url;
  }
  // 기존 이미지인 경우
  return store.API_URL + image.image;
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

// 수정 모드 시작 - 이미지 포함
const editArticle = (article) => {
  editingArticle.value = {
    ...article,
    originalImages: [...article.images], // 기존 이미지 백업
    images: [...article.images], // 수정할 이미지 배열
    newImages: [], // 새로 추가할 이미지 파일들
    removedImages: [], // 삭제된 기존 이미지 ID들
  };
  activeMenu.value = null;
};

// 수정 취소
const cancelEdit = () => {
  editingArticle.value = null;
};

// 수정 모드에서 이미지 업로드 처리
const handleEditImageUpload = (event) => {
  const files = Array.from(event.target.files);

  files.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      editingArticle.value.images.push({
        url: e.target.result,
        file: file,
        isNew: true, // 새로 추가된 이미지 표시
      });
      editingArticle.value.newImages.push(file);
    };
    reader.readAsDataURL(file);
  });
};

// 수정 모드에서 이미지 제거
const removeEditImage = (index) => {
  const removedImage = editingArticle.value.images[index];

  // 기존 이미지인 경우 삭제 목록에 추가
  if (!removedImage.isNew && removedImage.id) {
    editingArticle.value.removedImages.push(removedImage.id);
  }

  editingArticle.value.images.splice(index, 1);
};

// 이미지 제거
const removeImage = (index) => {
  newArticle.value.images.splice(index, 1);
};

// 게시글 등록(생성)
const submitArticle = () => {
  if (!newArticle.value.content.trim() && !newArticle.value.images.length) return;
  if (isSubmitting.value) return;

  isSubmitting.value = true;
  const formData = new FormData();
  formData.append("content", newArticle.value.content);

  // 이미지 파일들 추가
  newArticle.value.images.forEach((image, index) => {
    formData.append(`images`, image.file);
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
      // 성공적으로 게시글이 생성된 경우
      const newArticleData = response.data;

      // 게시글 목록 최상단에 새 게시글 추가
      articles.value = [
        {
          id: newArticleData.id,
          user: {
            id: newArticleData.user.id,
            name: newArticleData.user.name,
            profile_img: newArticleData.user.profile_img,
          },
          content: newArticleData.content,
          created_at: newArticleData.created_at,
          images: newArticleData.images.map((img) => ({ image: img.image })),
        },
        ...articles.value,
      ];

      emit("update:articles-images", newArticleData.images);

      // 폼 초기화
      newArticle.value = {
        content: "",
        images: [],
      };
      // 성공 메시지 표시
      alert("게시글이 성공적으로 등록되었습니다.");
    })
    .catch((error) => {
      console.error("게시글 등록 실패:", error);
    })
    .finally(() => {
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

.article-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
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
</style>
