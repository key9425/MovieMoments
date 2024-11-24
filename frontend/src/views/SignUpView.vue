<template>
  <main class="signup-container">
    <div class="signup-content">
      <!-- 타이틀 -->
      <div class="title-section">
        <h1 class="main-title">회원가입</h1>
        <p class="subtitle">영화같은 순간을 함께 나눠보세요</p>
      </div>

      <!-- 회원가입 폼 -->
      <div class="signup-box">
        <form @submit.prevent="signUp" class="signup-form">
          <div class="form-group">
            <input type="text" id="name" v-model.trim="name" placeholder="이름" class="form-input" />
          </div>

          <div class="form-group">
            <input type="email" id="email" v-model.trim="email" placeholder="이메일" class="form-input" />
          </div>

          <div class="form-group">
            <input type="text" id="username" v-model.trim="username" placeholder="아이디" class="form-input" />
            <p class="input-guide">한글/영문/숫자 10자까지</p>
          </div>

          <div class="form-group">
            <input type="password" id="password1" v-model.trim="password1" placeholder="비밀번호" class="form-input" />
            <p class="input-guide">영문/숫자/특수문자 조합 8자 이상</p>
          </div>

          <div class="form-group">
            <input type="password" id="password2" v-model.trim="password2" placeholder="비밀번호 확인" class="form-input" />
          </div>

          <button type="submit" class="submit-btn">가입하기</button>
        </form>

        <div class="login-section">
          <span>이미 계정이 있으신가요?</span>
          <RouterLink to="/" class="login-link">로그인</RouterLink>
        </div>
      </div>
    </div>

    <img src="@/assets/logo-img.svg" alt="메인 캐릭터" class="hero-image" />
  </main>
</template>

<style scoped>
.signup-container {
  min-height: 100vh;
  background-color: #f8f9fa;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.signup-content {
  width: 100%;
  max-width: 460px;
  padding: 0 2rem;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

/* 타이틀 섹션 */
.title-section {
  text-align: center;
  margin-bottom: 2.5rem;
}

.main-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.subtitle {
  font-size: 1.1rem;
  color: #6c757d;
}

/* 회원가입 폼 */
.signup-box {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 1rem 1.25rem;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  font-size: 1rem;
  color: #495057;
  transition: all 0.2s ease;
}

.form-input::placeholder {
  color: #adb5bd;
}

.form-input:focus {
  outline: none;
  border-color: #dc3545;
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
}

.input-guide {
  font-size: 0.8rem;
  color: #868e96;
  margin-top: 0.5rem;
  margin-left: 0.5rem;
}

.submit-btn {
  margin-top: 0.5rem;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  background-color: #dc3545;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover {
  background-color: #c82333;
  transform: translateY(-1px);
}

/* 로그인 링크 섹션 */
.login-section {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.95rem;
  color: #6c757d;
}

.login-link {
  color: #dc3545;
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.5rem;
  transition: color 0.2s ease;
}

.login-link:hover {
  color: #c82333;
}

/* 히어로 이미지 */
.hero-image {
  position: absolute;
  bottom: -150px;
  right: -150px;
  width: 30%;
  z-index: 1;
  opacity: 0.8;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .signup-content {
    padding: 0 1.5rem;
  }

  .main-title {
    font-size: 2rem;
  }

  .signup-box {
    padding: 2rem;
  }

  .hero-image {
    width: 300px;
    right: -50px;
    bottom: -50px;
  }
}

@media (max-width: 480px) {
  .signup-content {
    padding: 0 1rem;
  }

  .main-title {
    font-size: 1.75rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .signup-box {
    padding: 1.5rem;
  }

  .hero-image {
    width: 200px;
    right: -30px;
    bottom: -30px;
  }
}
</style>
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
