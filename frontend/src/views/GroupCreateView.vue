<template>
  <div class="container mt-5">
    <div class="text-center mb-4">
      <h1 class="display-5 mb-3">그룹 생성</h1>
      <p class="text-muted">나만의 영화메이트를 만들어서 순간을 기록하세요!</p>
    </div>

    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-body">
            <!-- 그룹명 -->
            <div class="mb-3">
              <label for="groupName" class="form-label">그룹명</label>
              <input type="text" class="form-control" id="groupName" v-model.trim="groupData.name" placeholder="그룹의 이름을 입력해주세요." required />
            </div>

            <!-- 그룹소개 -->
            <div class="mb-3">
              <label for="groupDescription" class="form-label">그룹소개</label>
              <textarea class="form-control" id="groupDescription" v-model.trim="groupData.description" rows="3" placeholder="그룹에 대한 간단한 소개글을 작성해주세요." required></textarea>
            </div>

            <!-- 그룹 대표 이미지 -->
            <div class="mb-3">
              <label for="groupImage" class="form-label">그룹 대표 이미지</label>
              <div class="image-upload-container">
                <div class="preview-container mb-2" v-if="imagePreview">
                  <img :src="imagePreview" alt="Preview" />
                </div>
                <input type="file" class="form-control" id="groupImage" @change="handleImageChange" accept="image/*" />
              </div>
            </div>

            <!-- 카테고리 선택 -->
            <div class="mb-4">
              <label class="form-label">카테고리 선택</label>
              <div class="d-flex flex-wrap gap-3">
                <div v-for="category in categories" :key="category.id" class="form-check">
                  <input class="form-check-input" type="radio" name="category" :id="'category-' + category.id" :value="category.id" v-model="groupData.category" />
                  <label class="form-check-label" :for="'category-' + category.id">
                    {{ category.name }}
                  </label>
                </div>
              </div>
            </div>

            <!-- 멤버 검색 및 선택 -->
            <div class="mb-4">
              <label class="form-label">멤버 추가</label>
              <input type="text" class="form-control mb-2" v-model="searchQuery" placeholder="이메일 혹은 이름으로 검색" />

              <!-- 검색 결과 -->
              <div v-if="searchResults.length" class="search-results mb-3">
                <div v-for="user in searchResults" :key="user.id" class="user-item" :class="{ selected: selectedUsers.includes(user.id) }" @click="toggleUserSelection(user)">
                  <p class="mb-1">{{ user.email }}</p>
                  <p class="mb-0">{{ user.name }}</p>
                </div>
              </div>

              <!-- 선택된 멤버 목록 -->
              <div v-if="selectedUsers.length" class="selected-users">
                <p class="mb-2">선택된 멤버</p>
                <ul class="list-unstyled">
                  <li v-for="userId in selectedUsers" :key="userId">ID: {{ userId }}</li>
                </ul>
              </div>
            </div>

            <!-- 제출 버튼 -->
            <div class="d-grid">
              <button type="button" class="btn btn-primary" @click="handleSubmit">그룹 생성하기</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import { useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const router = useRouter();
const store = useCounterStore();
const imagePreview = ref(null);
const searchQuery = ref("");
const searchResults = ref([]);
const selectedUsers = ref([]);

const groupData = reactive({
  name: "",
  description: "",
  image: null,
  category: "",
  members: [],
});

const categories = [
  { id: 1, name: "가족" },
  { id: 2, name: "연인" },
  { id: 3, name: "친구" },
  { id: 4, name: "직장" },
  { id: 5, name: "SSAFY" },
  { id: 6, name: "기타" },
];

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
      // 현재 로그인한 사용자를 제외한 검색 결과만 필터링
      searchResults.value = response.data.filter((user) => user.id !== store.currentUser.id);
    })
    .catch((error) => {
      console.error("사용자 검색 실패:", error);
    });
});

const toggleUserSelection = (user) => {
  const index = selectedUsers.value.indexOf(user.id);
  if (index === -1) {
    selectedUsers.value.push(user.id);
    groupData.members = [...selectedUsers.value];
  } else {
    selectedUsers.value.splice(index, 1);
    groupData.members = [...selectedUsers.value];
  }
};

const handleSubmit = async () => {
  try {
    const formData = new FormData();

    formData.append("group_name", groupData.name);
    formData.append("description", groupData.description);
    formData.append("category", groupData.category);

    if (groupData.image) {
      formData.append("group_img", groupData.image);
    }

    if (selectedUsers.value.length > 0) {
      selectedUsers.value.forEach((userId) => {
        formData.append("members", userId.toString());
      });
    }

    console.log("Sending data:");
    for (let [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }

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
    router.push({ name: "HomeView" });
  } catch (error) {
    console.error("그룹 생성 실패:", error.response?.data || error.message);
    if (error.response) {
      console.log("Error response:", error.response.data);
    }
  }
};
</script>

<style scoped>
.search-results {
  border: 1px solid #ddd;
  border-radius: 4px;
}

.user-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-item:hover {
  background-color: #f5f5f5;
}

.user-item.selected {
  background-color: #e3f2fd;
}

.user-item:last-child {
  border-bottom: none;
}

.selected-users {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.preview-container img {
  max-width: 100%;
  max-height: 200px;
  object-fit: contain;
}

.form-check {
  margin-right: 1rem;
}
</style>
