<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h1 class="modal-title">그룹 생성</h1>

      <div class="form-section">
        <!-- 그룹명 -->
        <div class="form-group">
          <label>그룹명</label>
          <input type="text" v-model="groupData.name" placeholder="모임!" class="input-field" />
        </div>

        <!-- 그룹 소개 -->
        <div class="form-group">
          <label>그룹 소개</label>
          <textarea v-model="groupData.description" placeholder="그룹에 대한 간단한 소개글을 작성해주세요." class="textarea-field" rows="4"></textarea>
        </div>

        <!-- 대표 이미지 -->
        <div class="form-group">
          <label>대표 이미지</label>
          <div class="image-upload-area" @click="triggerFileInput">
            <div v-if="imagePreview" class="preview-container">
              <img :src="imagePreview" alt="Preview" />
            </div>
            <div v-else class="upload-placeholder">
              <span class="plus-icon">+</span>
            </div>
            <input type="file" ref="fileInput" @change="handleImageChange" accept="image/*" class="hidden-input" />
          </div>
        </div>

        <!-- 영화메이트 -->
        <div class="form-group">
          <label>영화메이트</label>
          <input type="text" v-model="searchQuery" placeholder="검색" class="search-input" />
          <!-- 검색 결과 -->
          <div class="search-results" v-if="searchResults.length">
            <div v-for="user in searchResults" :key="user.id" class="user-item" @click="toggleUserSelection(user)">
              <div class="user-icon">👤</div>
              <div class="user-info">
                <div class="user-name">{{ user.name }}</div>
                <div class="user-email">{{ user.email }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 카테고리 -->
        <div class="form-group">
          <label>카테고리</label>
          <div class="category-container">
            <button
              v-for="category in categories"
              :key="category.id"
              @click="selectCategory(category.id)"
              class="category-btn"
              :class="{
                'category-family': category.name === '가족',
                'category-couple': category.name === '연인',
                'category-friend': category.name === '친구',
                'category-work': category.name === '직장',
                'category-ssafy': category.name === 'SSAFY',
                'category-etc': category.name === '기타',
              }"
            >
              {{ category.name }}
            </button>
          </div>
        </div>

        <!-- 생성 버튼 -->
        <button @click="handleSubmit" class="submit-btn">완료</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 32px;
  border-radius: 8px;
}

.modal-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.input-field,
.textarea-field,
.search-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background-color: #f8f9fa;
}

.image-upload-area {
  width: 150px;
  height: 150px;
  border: 2px solid #eee;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background-color: #fff;
}

.plus-icon {
  font-size: 32px;
  color: #333;
}

.preview-container {
  width: 100%;
  height: 100%;
}

.preview-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.search-results {
  margin-top: 8px;
  border: 1px solid #eee;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.user-item:last-child {
  border-bottom: none;
}

.user-icon {
  margin-right: 12px;
  font-size: 20px;
}

.user-name {
  font-weight: 500;
}

.user-email {
  font-size: 12px;
  color: #666;
}

.category-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
}

.category-family {
  background-color: #e9fae9;
}
.category-couple {
  background-color: #fae9e9;
}
.category-friend {
  background-color: #e9eafa;
}
.category-work {
  background-color: #faf6e9;
}
.category-ssafy {
  background-color: #f2e9fa;
}
.category-etc {
  background-color: #e9fafa;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background-color: #666;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 16px;
}

.hidden-input {
  display: none;
}
</style>

<script setup>
import { ref, reactive, watch } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const emit = defineEmits(["close", "group-created"]);
const fileInput = ref(null);

const imagePreview = ref(null);
const searchQuery = ref("");
const searchResults = ref([]);
const selectedUsers = ref([]);

const categories = [
  { id: 1, name: "가족" },
  { id: 2, name: "연인" },
  { id: 3, name: "친구" },
  { id: 4, name: "직장" },
  { id: 5, name: "SSAFY" },
  { id: 6, name: "기타" },
];

const groupData = reactive({
  name: "",
  description: "",
  image: null,
  category: "",
  members: [],
});

const handleImageChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    groupData.image = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const selectCategory = (categoryId) => {
  groupData.category = categoryId;
};

watch(searchQuery, (newQuery) => {
  if (!newQuery.trim()) {
    searchResults.value = [];
    return;
  }

  axios({
    method: "get",
    url: `${store.API_URL}/api/v2/search/`,
    params: { query: newQuery },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      searchResults.value = response.data.filter((user) => user.id !== store.currentUser.id);
    })
    .catch((error) => {
      console.error("사용자 검색 실패:", error);
    });
});

const toggleUserSelection = (user) => {
  const index = selectedUsers.value.findIndex((u) => u.id === user.id);
  if (index === -1) {
    selectedUsers.value.push(user);
    groupData.members.push(user.id);
  } else {
    selectedUsers.value.splice(index, 1);
    groupData.members = groupData.members.filter((id) => id !== user.id);
  }
};

const handleSubmit = async () => {
  const formData = new FormData();

  formData.append("group_name", groupData.name);
  formData.append("description", groupData.description);
  formData.append("category", groupData.category);

  if (groupData.image) {
    formData.append("group_img", groupData.image);
  }

  if (groupData.members.length > 0) {
    groupData.members.forEach((userId) => {
      formData.append("members", userId.toString());
    });
  }

  try {
    const response = await axios({
      method: "post",
      url: `${store.API_URL}/api/v1/groups/`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Token ${store.token}`,
      },
    });

    console.log("그룹 생성 성공:", response.data);
    emit("group-created");
  } catch (error) {
    console.error("그룹 생성 실패:", error.response?.data || error.message);
  }
};
</script>
