<template>
  <div class="signup-container">
    <h1>회원가입</h1>

    <div class="form-card">
      <form @submit.prevent="signUp" class="signup-form">
        <div class="input-field">
          <label for="name">이름</label>
          <input type="text" id="name" v-model.trim="name" placeholder="홍길동" />
        </div>

        <div class="input-field">
          <label for="email">이메일</label>
          <input type="email" id="email" v-model.trim="email" placeholder="example@example.com" />
        </div>

        <div class="input-field">
          <label for="username">아이디</label>
          <input type="text" id="username" v-model.trim="username" placeholder="아이디를 입력해주세요." />
          <p class="input-guide">한글/영문/숫자 10자까지</p>
        </div>

        <div class="input-field">
          <label for="password1">비밀번호</label>
          <input type="password" id="password1" v-model.trim="password1" placeholder="비밀번호를 입력해주세요." />
          <p class="input-guide">영문/숫자/특수문자 조합 8자 이상</p>
        </div>

        <div class="input-field">
          <label for="password2">비밀번호 확인</label>
          <input type="password" id="password2" v-model.trim="password2" placeholder="비밀번호를 한 번 더 입력해주세요." />
        </div>

        <button type="submit" class="submit-btn">회원가입</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";

const name = ref(null);
const email = ref(null);
const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);

const store = useCounterStore();

const signUp = function () {
  // 클라이언트 측 유효성 검사
  if (!name.value) {
    alert("이름을 입력해주세요.");
    return;
  }
  if (!email.value) {
    alert("이메일을 입력해주세요.");
    return;
  }
  // 이메일 형식 검사
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.value)) {
    alert("올바른 이메일 형식이 아닙니다.");
    return;
  }
  if (!username.value) {
    alert("아이디를 입력해주세요.");
    return;
  }
  if (username.value.length > 10) {
    alert("아이디는 10자 이내로 입력해주세요.");
    return;
  }
  if (!password1.value) {
    alert("비밀번호를 입력해주세요.");
    return;
  }
  if (password1.value.length < 8) {
    alert("비밀번호는 8자 이상이어야 합니다.");
    return;
  }
  // 비밀번호 복잡성 검사
  // const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
  // if (!passwordRegex.test(password1.value)) {
  //   alert("비밀번호는 영문, 숫자, 특수문자를 모두 포함해야 합니다.");
  //   return;
  // }
  if (!password2.value) {
    alert("비밀번호 확인을 입력해주세요.");
    return;
  }
  if (password1.value !== password2.value) {
    alert("비밀번호가 일치하지 않습니다.");
    return;
  }

  const payload = {
    name: name.value,
    email: email.value,
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  };
  store
    .signUp(payload)
    .then(() => {
      // 성공 시 처리는 store에서 수행
    })
    .catch((error) => {
      alert(error.message);
    });
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#app {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>

<style scoped>
.signup-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

h1 {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 30px;
}

.form-card {
  background: #f2f2f2;
  padding: 40px;
  border-radius: 10px;
  width: 100%;
  max-width: 500px;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.input-field {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-field label {
  font-size: 16px;
  font-weight: 500;
}

.input-field input {
  padding: 15px;
  border-radius: 5px;
  border: none;
  font-size: 14px;
  width: 100%;
}

.input-field input::placeholder {
  color: #999;
}

.input-guide {
  font-size: 12px;
  color: #666;
  margin-top: -5px;
}

.submit-btn {
  margin-top: 10px;
  padding: 15px;
  background: gray;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .form-card {
    padding: 20px;
  }
}
</style>
