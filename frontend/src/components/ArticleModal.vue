<!-- ArticleModal.vue -->
<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-content">
      <h2>새 게시글 작성</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">제목</label>
          <input v-model="formData.title" type="text" id="title" required class="form-control" />
        </div>

        <div class="form-group">
          <label for="content">내용</label>
          <textarea v-model="formData.content" id="content" rows="5" required class="form-control"></textarea>
        </div>

        <div class="form-group">
          <label for="image">이미지</label>
          <input type="file" id="image" @change="handleImageUpload" accept="image/*" class="form-control" />
        </div>

        <div class="button-group">
          <button @click="saveArticle" type="submit" class="btn btn-primary">저장</button>
          <button type="button" @click="close" class="btn btn-secondary">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const props = defineProps(["id"]);

const emit = defineEmits(["submit", "close"]);
const isOpen = ref(false);
const formData = ref({
  title: "",
  content: "",
  image: null,
});

const store = useCounterStore();

const saveArticle = () => {
  axios({
    method: "post",
    url: `${store.API_KEY}/api/v1/groups/${props.id}/articles/`,
    data: formData,
  })
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.log(error);
    });
};

const handleImageUpload = (event) => {
  formData.value.image = event.target.files[0];
};

const handleSubmit = () => {
  emit("submit", formData.value);
  close();
};

const close = () => {
  formData.value = {
    title: "",
    content: "",
    image: null,
  };
  isOpen.value = false;
  emit("close");
};

const open = () => {
  isOpen.value = true;
};

defineExpose({ open, close });
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.25rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}
</style>
