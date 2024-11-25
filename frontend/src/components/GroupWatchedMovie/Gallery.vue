<template>
  <section v-if="currentTab === 'gallery'" class="gallery-section">
    <div class="gallery-grid">
      <div v-for="image in galleryImages" :key="image.id" class="gallery-item" @click="openImage(image)">
        <img :src="store.API_URL + image.image" :alt="image.description" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";

const props = defineProps({
  currentTab: {
    type: String,
    required: true,
  },
  galleryData: {
    type: Array,
    default: () => [], // 기본값으로 빈 배열 설정
  },
});

const galleryImages = ref([...props.galleryData]);
const fileInput = ref(null); // ref 정의
const store = useCounterStore();

// 파일 선택 트리거
const triggerFileInput = () => {
  fileInput.value?.click();
};

// 이미지 업로드 처리
const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // 이미지 파일 타입 체크
  if (!file.type.startsWith("image/")) {
    alert("이미지 파일만 업로드 가능합니다.");
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    galleryImages.value.push({
      id: Date.now(),
      url: e.target.result,
      description: file.name,
    });
  };
  reader.readAsDataURL(file);

  // 파일 input 초기화
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};
</script>


<style scoped>
/* 기존 갤러리 스타일 */
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
