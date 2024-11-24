<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- X 버튼 추가 -->
      <button class="close-btn" @click="$emit('close')">×</button>

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
              <!-- 이미지 삭제 버튼 추가 -->
              <button class="delete-image-btn" @click.stop="deleteImage">×</button>
            </div>
            <div v-else class="upload-placeholder">
              <span class="plus-icon">+</span>
            </div>
            <input type="file" ref="fileInput" @change="handleImageChange" accept="image/*" class="hidden-input" />
          </div>
        </div>

        <!-- 영화메이트 섹션 -->
        <div class="form-group">
          <label>영화메이트</label>
          <div class="search-input-container">
            <div class="selected-users-chips">
              <div v-for="user in selectedUsers" :key="user.id" class="user-chip">
                {{ user.name }}
                <button @click.stop="toggleUserSelection(user)" class="remove-user-btn">×</button>
              </div>
              <input type="text" v-model="searchQuery" placeholder="검색" class="search-input" :class="{ 'with-selections': selectedUsers.length > 0 }" />
            </div>
          </div>

          <!-- 검색 결과 -->
          <div class="search-results" v-if="searchResults.length">
            <div v-for="user in searchResults" :key="user.id" class="user-item" :class="{ 'user-selected': isUserSelected(user) }" @click="toggleUserSelection(user)">
              <img :src="store.API_URL + user.profile_img" alt="" class="profile-image" />
              <div class="user-info">
                <div class="user-name">{{ user.name }}</div>
                <div class="user-email">{{ user.email }}</div>
              </div>
              <div v-if="isUserSelected(user)" class="check-icon">✓</div>
            </div>
          </div>
        </div>

        <!-- 카테고리 섹션 -->
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
                selected: groupData.category === category.id,
              }"
            >
              {{ category.name }}
              <!-- <span v-if="groupData.category === category.id" class="category-check">✓</span> -->
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
  position: relative; /* 닫기 버튼의 절대 위치 기준점 */

  background-color: #fff;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 32px;
  border-radius: 8px;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 30px;
  height: 30px;
  border: none;
  background: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-btn:hover {
  background-color: #f0f0f0;
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

.textarea-field {
  height: 150px;
  resize: none;
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
  position: relative;
}

.preview-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

/* 이미지 삭제 버튼 스타일 추가 */
.delete-image-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #fff;
  border: 1px solid #ddd;
  color: #666;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.delete-image-btn:hover {
  background-color: #f0f0f0;
}

.search-results {
  margin-top: 4px;
  padding: 10px 0;
  border: 1px solid #eee;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.profile-image {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}
.user-item {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 12px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.user-item:hover {
  background-color: #f5f5f5;
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

/* 선택된 사용자 태그 스타일 */
.selected-users {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 8px 0;
}

.selected-user-tag {
  display: flex;
  align-items: center;
  background-color: #e8e8e8;
  padding: 4px 8px;
  border-radius: 16px;
  font-size: 14px;
}

.remove-user-btn {
  border: none;
  background: none;
  margin-left: 4px;
  cursor: pointer;
  color: #666;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-user-btn:hover {
  color: #333;
}

/* 검색 입력창 컨테이너 스타일 */
.search-input-container {
  position: relative;
  width: 100%;
}

.selected-users-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 8px;
  min-height: 48px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f8f9fa;
  align-items: center;
}

.user-chip {
  display: flex;
  align-items: center;
  background-color: #e8e8e8;
  padding: 4px 8px;
  border-radius: 16px;
  font-size: 14px;
  max-width: fit-content;
}

.search-input {
  border: none;
  outline: none;
  padding: 4px 8px;
  font-size: 14px;
  background: transparent;
  flex: 1;
  min-width: 120px;
}

.search-input.with-selections {
  margin-left: 4px;
}

.remove-user-btn {
  border: none;
  background: none;
  margin-left: 4px;
  cursor: pointer;
  color: #666;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

.remove-user-btn:hover {
  color: #333;
}

/* 사용자 아이템 선택 스타일 */
.user-item {
  position: relative;
  padding-right: 40px; /* 체크 아이콘 공간 확보 */
}

.user-selected {
  background-color: #f0f7ff;
}

.check-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #4caf50;
  font-weight: bold;
}

/* 카테고리 버튼 선택 스타일 */
.category-btn {
  position: relative;
  padding-right: 32px; /* 체크 아이콘 공간 확보 */
}

.category-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.category-family.selected {
  background-color: #d4f3d4;
}
.category-couple.selected {
  background-color: #f3d4d4;
}
.category-friend.selected {
  background-color: #d4d6f3;
}
.category-work.selected {
  background-color: #f3ecd4;
}
.category-ssafy.selected {
  background-color: #e6d4f3;
}
.category-etc.selected {
  background-color: #d4f3f3;
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

// 이미지 삭제 함수 추가
const deleteImage = () => {
  imagePreview.value = null;
  groupData.image = null;
  if (fileInput.value) {
    fileInput.value.value = ""; // 파일 input 초기화
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

// 사용자 선택 여부 확인 함수 추가
const isUserSelected = (user) => {
  return selectedUsers.value.some((selectedUser) => selectedUser.id === user.id);
};

// 카테고리 선택 함수
const selectCategory = (categoryId) => {
  // 이미 선택된 카테고리를 다시 클릭하면 선택 해제
  if (groupData.category === categoryId) {
    groupData.category = "";
  } else {
    groupData.category = categoryId;
  }
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
      console.log("사용자", searchResults.value);
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

const handleSubmit = () => {
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

  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/groups/`,
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log("그룹 생성 성공:", response.data);
      emit("group-created");
    })
    .catch((error) => {
      console.error("그룹 생성 실패:", error.response?.data || error.message);
    });
};
</script>
