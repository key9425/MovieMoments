<template>
  <section class="gallery-section">
    <!-- 라이트박스 -->
    <div v-if="selectedImage" class="lightbox" @click="closeLightbox">
      <div class="lightbox-container" @click.stop>
        <button class="close-button" @click="closeLightbox">&times;</button>

        <!-- 이전 버튼 -->
        <button class="nav-button prev" @click="navigateImage(-1)" :disabled="currentImageIndex === 0">&lt;</button>

        <!-- 이미지 컨테이너 -->
        <div class="image-container">
          <img :src="store.API_URL + selectedImage.image" :alt="selectedImage.description" />
        </div>

        <!-- 다음 버튼 -->
        <button class="nav-button next" @click="navigateImage(1)" :disabled="currentImageIndex === galleryImages.length - 1">&gt;</button>
      </div>
    </div>

    <!-- 기존 갤러리 그리드 -->
    <div class="gallery-grid">
      <div v-for="image in galleryImages" :key="image.id" class="gallery-item" @click="openImage(image)">
        <img :src="store.API_URL + image.image" :alt="image.description" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute } from "vue-router";
import axios from "axios";

const store = useCounterStore();
const route = useRoute();

// 갤러리 이미지 상태 관리
const galleryImages = ref([]);
const fileInput = ref(null);
const selectedImage = ref(null);
const currentImageIndex = ref(0);

// 갤러리 데이터 가져오기
const getGalleryImages = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      if (response.data.article_img) {
        galleryImages.value = response.data.article_img;
      }
    })
    .catch((error) => {
      console.error("갤러리 이미지 로드 실패:", error);
    });
};

// 라이트박스 관련 함수들
const openImage = (image) => {
  selectedImage.value = image;
  currentImageIndex.value = galleryImages.value.findIndex((img) => img.id === image.id);
};

const closeLightbox = () => {
  selectedImage.value = null;
};

const navigateImage = (direction) => {
  const newIndex = currentImageIndex.value + direction;
  if (newIndex >= 0 && newIndex < galleryImages.value.length) {
    currentImageIndex.value = newIndex;
    selectedImage.value = galleryImages.value[newIndex];
  }
};

// 파일 선택 트리거
const triggerFileInput = () => {
  fileInput.value?.click();
};

// 이미지 업로드 처리
const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  if (!file.type.startsWith("image/")) {
    alert("이미지 파일만 업로드 가능합니다.");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/group/movie/${route.params.group_movie_id}/gallery/`,
    headers: {
      Authorization: `Token ${store.token}`,
      "Content-Type": "multipart/form-data",
    },
    data: formData,
  })
    .then((response) => {
      galleryImages.value.push(response.data);
      if (fileInput.value) {
        fileInput.value.value = "";
      }
    })
    .catch((error) => {
      console.error("이미지 업로드 실패:", error);
      alert("이미지 업로드에 실패했습니다.");
    });
};

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  getGalleryImages();
});
</script>

<style scoped>
/* 기존 갤러리 스타일 유지 */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.gallery-item {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 12px;
  cursor: pointer;
  border: 1px solid #e1e1e1;
  background: #ffffff;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

/* 라이트박스 스타일 수정 */
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.lightbox-container {
  position: relative;
  width: 90vw;
  height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.image-container {
  height: 100%;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.close-button {
  position: fixed;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
  z-index: 1001;
}

.close-button:hover {
  background: rgba(0, 0, 0, 0.7);
}

.nav-button {
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 20px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-button:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.7);
  transform: scale(1.1);
}

.nav-button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* 이미지 추가 버튼 스타일 */
.add-image-item {
  cursor: pointer;
  background: #f8f9fa;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #e1e1e1;
}

.add-image-item:hover {
  background: #f1f3f5;
  border-color: #3a3a3a;
}

.add-image-btn {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  transition: color 0.3s ease;
}

.add-image-btn:hover {
  color: #3a3a3a;
}

.add-icon {
  font-size: 2rem;
  font-weight: 300;
  width: 50px;
  height: 50px;
  border: 2px solid currentColor;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
}

/* 드래그 앤 드롭 스타일 */
.add-image-item.dragging {
  background: #e9ecef;
  border-color: #3a3a3a;
}

@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }

  .add-icon {
    width: 40px;
    height: 40px;
    font-size: 1.5rem;
  }

  .add-image-btn span {
    font-size: 0.9rem;
  }
}
</style>
