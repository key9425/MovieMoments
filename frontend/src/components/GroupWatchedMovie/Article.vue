<template>
  <section class="article-section">
    <!-- 게시글 작성 폼 -->
    <div class="article-form-card">
      <h3 class="form-title">게시글 작성</h3>
      <form @submit.prevent="submitArticle" class="article-form">
        <div class="input-area">
          <textarea v-model="content" placeholder="특별한 순간을 기록해보세요." class="content-input" :maxlength="2000"></textarea>
          <div class="char-count" :class="{ 'near-limit': content.length > 1800 }">{{ content.length }}/2000</div>
        </div>

        <!-- 이미지 업로드 영역 -->
        <div class="image-upload-area">
          <label class="upload-label">
            <div class="upload-button">
              <i class="fas fa-image"></i>
              <span>사진 추가</span>
              <span class="image-count" v-if="images.length">({{ images.length }}/10)</span>
            </div>
            <input type="file" accept="image/*" multiple @change="handleImageUpload" class="hidden" ref="fileInput" />
          </label>

          <!-- 이미지 미리보기 -->
          <div v-if="imagePreviews.length" class="image-preview-grid">
            <div v-for="(preview, index) in imagePreviews" :key="index" class="preview-item">
              <img :src="preview" :alt="`Preview ${index + 1}`" />
              <button @click.prevent="removeImage(index)" class="remove-image-btn" aria-label="이미지 제거">
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="submit-btn" :disabled="!content.trim() || isSubmitting">
            <i class="fas fa-paper-plane"></i>
            게시하기
          </button>
        </div>
      </form>
    </div>

    <!-- 게시글 목록 -->
    <div class="articles-container">
      <div v-if="!articles.length" class="empty-state">
        <i class="fas fa-pen-fancy empty-icon"></i>
        <p>아직 작성된 게시글이 없습니다. 첫 번째 게시글을 작성해보세요!</p>
      </div>

      <article v-for="article in articles" :key="article.id" class="article-card" :class="{ 'fade-enter': article.isNew }">
        <!-- 게시글 헤더 -->
        <div class="article-header">
          <div class="user-info">
            <img :src="store.API_URL + article.user.profile_img" :alt="article.user.name" class="user-avatar" loading="lazy" />
            <div class="user-details">
              <span class="user-name">{{ article.user.name }}</span>
              <span class="post-date">{{ formatDate(article.created_at) }}</span>
            </div>
          </div>

          <!-- 수정/삭제 메뉴 -->
          <div v-if="article.user.id === store.currentUser?.id" class="article-actions">
            <button class="action-btn" @click="startEdit(article)" aria-label="게시글 수정">
              <i class="fas fa-edit"></i>
            </button>
            <button class="action-btn delete" @click="deleteArticle(article.id)" aria-label="게시글 삭제">
              <i class="fas fa-trash-alt"></i>
            </button>
          </div>
        </div>

        <!-- 게시글 내용 -->
        <div v-if="editingId === article.id">
          <!-- 수정 폼 -->
          <div class="edit-form">
            <textarea v-model="editingContent" class="content-input" :maxlength="2000"></textarea>

            <!-- 이미지 업로드 영역 -->
            <div class="image-upload-area">
              <label class="upload-label">
                <div class="upload-button">
                  <i class="fas fa-image"></i>
                  <span>사진 추가</span>
                  <span class="image-count" v-if="editingImages.length">({{ editingImages.length }}/10)</span>
                </div>
                <input type="file" accept="image/*" multiple @change="handleEditImageUpload" class="hidden" />
              </label>

              <!-- 이미지 미리보기 -->
              <div v-if="editingImagePreviews.length" class="image-preview-grid">
                <div v-for="(preview, index) in editingImagePreviews" :key="index" class="preview-item">
                  <img :src="preview" :alt="`Preview ${index + 1}`" />
                  <button @click.prevent="removeEditImage(index)" class="remove-image-btn" aria-label="이미지 제거">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
              </div>
            </div>

            <div class="edit-actions">
              <button @click="updateArticle(article.id)" class="save-btn">저장</button>
              <button @click="cancelEdit" class="cancel-btn">취소</button>
            </div>
          </div>
        </div>
        <div v-else>
          <!-- 일반 표시 모드 -->
          <p class="article-content">{{ article.content }}</p>

          <!-- 이미지 그리드 -->
          <div v-if="article.images?.length" class="image-grid">
            <div v-for="(image, index) in article.images" :key="index" class="image-item" @click="openLightbox(article.images, index)">
              <img :src="store.API_URL + image.image" :alt="`Image ${index + 1}`" loading="lazy" />
            </div>
          </div>

          <!-- 댓글 섹션 -->
          <div class="comments-section">
            <button class="toggle-comments-btn" @click="toggleComments(article.id)">
              <i class="fas fa-comment"></i>
              댓글 {{ article.comments?.length || 0 }}개
            </button>

            <div v-show="activeComments === article.id" class="comments-container">
              <!-- 댓글 입력 -->
              <div class="comment-form">
                <textarea v-model="commentContent[article.id]" placeholder="댓글을 입력하세요..." class="comment-input" @keyup.enter="submitComment(article.id)"></textarea>
                <button @click="submitComment(article.id)" class="comment-submit-btn" :disabled="!commentContent[article.id]?.trim()">등록</button>
              </div>

              <!-- 댓글 목록 -->
              <div class="comments-list">
                <div v-for="comment in article.comments" :key="comment.id" class="comment-item">
                  <div class="comment-header">
                    <div class="comment-user-info">
                      <img :src="store.API_URL + comment.user.profile_img" :alt="comment.user.name" class="comment-avatar" />
                      <span class="comment-user-name">{{ comment.user.name }}</span>
                      <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                    </div>
                    <button v-if="comment.user.id === store.currentUser?.id" @click="deleteComment(article.id, comment.id)" class="delete-comment-btn">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                  <p class="comment-content">{{ comment.content }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- Lightbox -->
    <div v-if="lightbox.visible" class="lightbox" @click="closeLightbox">
      <div class="lightbox-content" @click.stop>
        <button class="close-lightbox" @click="closeLightbox">
          <i class="fas fa-times"></i>
        </button>
        <img :src="store.API_URL + lightbox.images[lightbox.currentIndex].image" :alt="'Image view'" />
        <button v-if="lightbox.currentIndex > 0" class="nav-btn prev" @click="navigateImage(-1)">
          <i class="fas fa-chevron-left"></i>
        </button>
        <button v-if="lightbox.currentIndex < lightbox.images.length - 1" class="nav-btn next" @click="navigateImage(1)">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const store = useCounterStore();
const route = useRoute();

// 상태 관리
const articles = ref([]);
const content = ref("");
const images = ref([]);
const imagePreviews = ref([]);
const isSubmitting = ref(false);
const editingId = ref(null);
const editingContent = ref("");
const activeComments = ref(null);
const commentContent = ref({});
const lightbox = ref({
  visible: false,
  images: [],
  currentIndex: 0,
});
const editingImages = ref([]);
const editingImagePreviews = ref([]);
const removedImageIds = ref([]);

// 게시글 조회
const getArticles = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/articles/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    articles.value = response.data;
  } catch (error) {
    console.error("게시글 조회 실패:", error);
  }
};

// 이미지 처리
const handleImageUpload = (event) => {
  const files = Array.from(event.target.files);
  const maxFiles = 10 - images.value.length;

  if (files.length > maxFiles) {
    alert(`이미지는 최대 ${maxFiles}개까지 추가할 수 있습니다.`);
    return;
  }

  files.forEach((file) => {
    if (file.size > 5 * 1024 * 1024) {
      alert("파일 크기는 5MB를 초과할 수 없습니다.");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreviews.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
    images.value.push(file);
  });
};

const removeImage = (index) => {
  URL.revokeObjectURL(imagePreviews.value[index]);
  images.value.splice(index, 1);
  imagePreviews.value.splice(index, 1);
};

// 게시글 작성
const submitArticle = async () => {
  if (!content.value.trim() || isSubmitting.value) return;

  isSubmitting.value = true;
  const formData = new FormData();
  formData.append("content", content.value);

  images.value.forEach((file) => {
    formData.append("images", file);
  });

  try {
    const response = await axios({
      method: "post",
      url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/articles/`,
      headers: {
        Authorization: `Token ${store.token}`,
        "Content-Type": "multipart/form-data",
      },
      data: formData,
    });

    // 새 게시글 추가
    articles.value.unshift({
      ...response.data,
      isNew: true,
    });

    // 입력폼 초기화
    content.value = "";
    images.value = [];
    imagePreviews.value = [];

    // 애니메이션 플래그 제거
    setTimeout(() => {
      const index = articles.value.findIndex((a) => a.id === response.data.id);
      if (index !== -1) {
        articles.value[index] = { ...articles.value[index], isNew: false };
      }
    }, 300);
  } catch (error) {
    console.error("게시글 작성 실패:", error);
    alert("게시글 작성에 실패했습니다.");
  } finally {
    isSubmitting.value = false;
  }
};

// 게시글 수정
const startEdit = (article) => {
  editingId.value = article.id;
  editingContent.value = article.content;

  editingImages.value = article.images.map((img) => ({
    id: img.id,
    image: img.image,
    isExisting: true,
  }));
  editingImagePreviews.value = article.images.map((img) => store.API_URL + img.image);
  removedImageIds.value = [];
};

const emit = defineEmits(["article-updated"]);

// updateArticle 함수 수정
const updateArticle = async (articleId) => {
  if (!editingContent.value.trim()) return;

  const formData = new FormData();
  formData.append("content", editingContent.value);

  // 새로운 이미지만 필터링하여 추가
  editingImages.value
    .filter((image) => !image.isExisting)
    .forEach((image) => {
      formData.append("images", image.file);
    });

  // 삭제할 이미지 ID 추가
  removedImageIds.value.forEach((id) => {
    formData.append("removed_image_ids", id);
  });

  try {
    const response = await axios({
      method: "put",
      url: `${store.API_URL}/api/v1/group/movie/article/${articleId}/`,
      headers: {
        Authorization: `Token ${store.token}`,
        "Content-Type": "multipart/form-data",
      },
      data: formData,
    });

    const index = articles.value.findIndex((a) => a.id === articleId);
    if (index !== -1) {
      articles.value[index] = response.data;
    }

    // 수정 모드 종료 및 상태 초기화
    editingId.value = null;
    editingContent.value = "";
    editingImages.value = [];
    editingImagePreviews.value = [];
    removedImageIds.value = [];

    // 부모 컴포넌트에 업데이트 알림 추가
    emit("article-updated");
  } catch (error) {
    console.error("게시글 수정 실패:", error);
    alert("게시글 수정에 실패했습니다.");
  }
};

const cancelEdit = () => {
  editingId.value = null;
  editingContent.value = "";
};

// 게시글 삭제
const deleteArticle = async (articleId) => {
  if (!confirm("이 게시글을 삭제하시겠습니까?")) return;

  try {
    await axios({
      method: "delete",
      url: `${store.API_URL}/api/v1/group/movie/article/${articleId}/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    articles.value = articles.value.filter((article) => article.id !== articleId);
  } catch (error) {
    console.error("게시글 삭제 실패:", error);
    alert("게시글 삭제에 실패했습니다.");
  }
};

// 이미지 수정 처리 함수 추가
const handleEditImageUpload = (event) => {
  const files = Array.from(event.target.files);
  const maxFiles = 10 - editingImages.value.length;

  if (files.length > maxFiles) {
    alert(`이미지는 최대 ${maxFiles}개까지 추가할 수 있습니다.`);
    return;
  }

  files.forEach((file) => {
    if (file.size > 5 * 1024 * 1024) {
      alert("파일 크기는 5MB를 초과할 수 없습니다.");
      return;
    }

    editingImages.value.push({
      file,
      isExisting: false,
    });

    const reader = new FileReader();
    reader.onload = (e) => {
      editingImagePreviews.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });
};

// 수정 시 이미지 제거 함수 추가
const removeEditImage = (index) => {
  const removedImage = editingImages.value[index];
  if (removedImage.isExisting) {
    removedImageIds.value.push(removedImage.id);
  }
  URL.revokeObjectURL(editingImagePreviews.value[index]);
  editingImages.value.splice(index, 1);
  editingImagePreviews.value.splice(index, 1);
};

// 댓글 관련 기능
const toggleComments = async (articleId) => {
  if (activeComments.value === articleId) {
    activeComments.value = null;
  } else {
    activeComments.value = articleId;
    if (!articles.value.find((a) => a.id === articleId).comments) {
      await loadComments(articleId);
    }
  }
};

const loadComments = async (articleId) => {
  try {
    const response = await axios({
      method: "get",
      url: `${store.API_URL}/api/v1/group/movie/${articleId}/comments/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    const articleIndex = articles.value.findIndex((a) => a.id === articleId);
    if (articleIndex !== -1) {
      articles.value[articleIndex] = {
        ...articles.value[articleIndex],
        comments: response.data,
      };
    }
  } catch (error) {
    console.error("댓글 로드 실패:", error);
  }
};

const submitComment = async (articleId) => {
  if (!commentContent.value[articleId]?.trim()) return;

  try {
    const response = await axios({
      method: "post",
      url: `${store.API_URL}/api/v1/group/movie/${articleId}/comments/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
      data: {
        content: commentContent.value[articleId],
      },
    });

    const articleIndex = articles.value.findIndex((a) => a.id === articleId);
    if (articleIndex !== -1) {
      if (!articles.value[articleIndex].comments) {
        articles.value[articleIndex].comments = [];
      }
      articles.value[articleIndex].comments.push(response.data);
    }

    commentContent.value[articleId] = "";
  } catch (error) {
    console.error("댓글 작성 실패:", error);
    alert("댓글 작성에 실패했습니다.");
  }
};

const deleteComment = async (articleId, commentId) => {
  if (!confirm("이 댓글을 삭제하시겠습니까?")) return;

  try {
    await axios({
      method: "delete",
      url: `${store.API_URL}/api/v1/group/movie/${articleId}/comments/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
      data: { comment_id: commentId },
    });

    const articleIndex = articles.value.findIndex((a) => a.id === articleId);
    if (articleIndex !== -1) {
      articles.value[articleIndex].comments = articles.value[articleIndex].comments.filter((comment) => comment.id !== commentId);
    }
  } catch (error) {
    console.error("댓글 삭제 실패:", error);
    alert("댓글 삭제에 실패했습니다.");
  }
};

// Lightbox 관련 기능
const openLightbox = (images, index) => {
  lightbox.value = {
    visible: true,
    images: images,
    currentIndex: index,
  };
  document.body.style.overflow = "hidden";
};

const closeLightbox = () => {
  lightbox.value.visible = false;
  document.body.style.overflow = "auto";
};

const navigateImage = (direction) => {
  const newIndex = lightbox.value.currentIndex + direction;
  if (newIndex >= 0 && newIndex < lightbox.value.images.length) {
    lightbox.value.currentIndex = newIndex;
  }
};

// 유틸리티 함수
const formatDate = (date) => {
  return new Date(date).toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

// 이벤트 리스너
const handleEscape = (e) => {
  if (e.key === "Escape" && lightbox.value.visible) {
    closeLightbox();
  }
};

onMounted(() => {
  getArticles();
  window.addEventListener("keydown", handleEscape);
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleEscape);
  imagePreviews.value.forEach((url) => URL.revokeObjectURL(url));
});
</script>

<style scoped>
.article-section {
  padding: 1rem 0;
}

/* 폼 스타일 */
.article-form-card {
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

.article-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-area {
  position: relative;
}

.content-input {
  width: 100%;
  min-height: 120px;
  padding: 1rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  background: #f8f9fa;
  resize: vertical;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.content-input:focus {
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

/* 이미지 업로드 영역 */
.image-upload-area {
  margin-top: 1.5rem;
}

.upload-label {
  cursor: pointer;
}

.upload-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1rem;
  border: 1px dashed #e1e1e1;
  border-radius: 8px;
  color: #666;
  transition: all 0.2s ease;
}

.upload-button:hover {
  border-color: #dc3545;
  color: #dc3545;
}

.image-count {
  color: #6c757d;
  font-size: 0.9rem;
}

.hidden {
  display: none;
}

.image-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.remove-image-btn:hover {
  background: rgba(220, 53, 69, 0.8);
}

/* 버튼 스타일 */
.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.8rem;
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

/* 게시글 카드 스타일 */
.articles-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.article-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  opacity: 1;
  transform: translateY(0);
}

.article-card.fade-enter {
  opacity: 0;
  transform: translateY(-20px);
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
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: #333;
}

.post-date {
  font-size: 0.8rem;
  color: #6c757d;
}

.article-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: none;
  border: none;
  color: #6c757d;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  color: #333;
  transform: scale(1.1);
}

.action-btn.delete:hover {
  color: #dc3545;
}

/* 이미지 그리드 */
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.5rem;
  margin: 1rem 0;
}

.image-item {
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.2s ease;
}

.image-item:hover img {
  transform: scale(1.05);
}

/* 댓글 섹션 */
.comments-section {
  margin-top: 1rem;
  border-top: 1px solid #e1e1e1;
  padding-top: 1rem;
}

.toggle-comments-btn {
  background: none;
  border: none;
  color: #6c757d;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.toggle-comments-btn:hover {
  color: #333;
}

.comments-container {
  margin-top: 1rem;
}

.comment-form {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.comment-input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  background: #f8f9fa;
  resize: none;
  min-height: 40px;
}

.comment-input:focus {
  outline: none;
  border-color: #dc3545;
  background: white;
}

.comment-submit-btn {
  padding: 0 1.5rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.comment-submit-btn:hover:not(:disabled) {
  background: #c82333;
}

.comment-item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.comment-user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.comment-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.comment-user-name {
  font-weight: 500;
  font-size: 0.9rem;
}

.comment-date {
  font-size: 0.8rem;
  color: #6c757d;
}

.delete-comment-btn {
  background: none;
  border: none;
  color: #dc3545;
  opacity: 0.5;
  cursor: pointer;
  padding: 0.25rem;
  transition: all 0.2s ease;
}

.delete-comment-btn:hover {
  opacity: 1;
  transform: scale(1.1);
}

/* Lightbox 스타일 */
.lightbox {
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

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.lightbox-content img {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
}

.close-lightbox {
  position: absolute;
  top: -2rem;
  right: -2rem;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: transform 0.2s ease;
}

.close-lightbox:hover {
  transform: scale(1.1);
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn:hover {
  background: rgba(0, 0, 0, 0.8);
  transform: translateY(-50%) scale(1.1);
}

.nav-btn.prev {
  left: 1rem;
  border-radius: 50% 0 0 50%;
}

.nav-btn.next {
  right: 1rem;
  border-radius: 0 50% 50% 0;
}

/* Empty state */
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

/* 수정 폼 */
.edit-form {
  margin: 1rem 0;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.save-btn,
.cancel-btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.save-btn {
  background: #dc3545;
  color: white;
}

.save-btn:hover {
  background: #c82333;
}

.cancel-btn {
  background: #e9ecef;
  color: #495057;
}

.cancel-btn:hover {
  background: #dde2e6;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .article-section {
    padding: 1rem;
  }

  .article-form-card {
    padding: 1rem;
  }

  .input-group {
    flex-direction: column;
  }

  .submit-btn {
    width: 100%;
  }

  .image-preview-grid {
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
    gap: 0.5rem;
  }

  .image-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }

  .comment-form {
    flex-direction: column;
  }

  .comment-submit-btn {
    width: 100%;
    padding: 0.8rem;
  }

  .nav-btn {
    padding: 0.8rem;
  }

  .close-lightbox {
    top: -3rem;
    right: 0;
  }
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-enter {
  animation: fadeIn 0.3s ease forwards;
}
</style>
