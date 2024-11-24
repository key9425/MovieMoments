<template>
  <main class="login-container">
    <div class="login-content">
      <!-- 로고 & 타이틀 -->
      <div class="title-section">
        <h1 class="main-title">영화처럼, 순간처럼</h1>
        <p class="subtitle">당신의 모든 순간과 함께합니다</p>
      </div>

      <!-- 로그인 폼 -->
      <div class="login-box">
        <form @submit.prevent="logIn" class="login-form">
          <div class="form-group">
            <input type="text" id="username" v-model="credentials.username" placeholder="아이디" class="form-input" />
          </div>

          <div class="form-group">
            <input type="password" id="password" v-model="credentials.password" placeholder="비밀번호" class="form-input" />
          </div>

          <button type="submit" class="login-btn">로그인</button>
        </form>

        <div class="signup-section">
          <span>계정이 없으신가요?</span>
          <RouterLink to="/signup" class="signup-link">회원가입</RouterLink>
        </div>
      </div>
    </div>

    <img src="@/assets/logo-img.svg" alt="메인 캐릭터" class="hero-image" />
  </main>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  background-color: #f8f9fa;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-content {
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

/* 로그인 폼 */
.login-box {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

.login-btn {
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

.login-btn:hover {
  background-color: #c82333;
  transform: translateY(-1px);
}

/* 회원가입 섹션 */
.signup-section {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.95rem;
  color: #6c757d;
}

.signup-link {
  color: #dc3545;
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.5rem;
  transition: color 0.2s ease;
}

.signup-link:hover {
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
  .login-content {
    padding: 0 1.5rem;
  }

  .main-title {
    font-size: 2rem;
  }

  .login-box {
    padding: 2rem;
  }

  .hero-image {
    width: 300px;
    right: -50px;
    bottom: -50px;
  }
}

@media (max-width: 480px) {
  .login-content {
    padding: 0 1rem;
  }

  .main-title {
    font-size: 1.75rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .login-box {
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
import { useRouter, RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const router = useRouter();
const store = useCounterStore();

const credentials = ref({
  username: "",
  password: "",
});

const logIn = function () {
  store.logIn(credentials.value);
};
</script>
