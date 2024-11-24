<template>
  <main class="login-main">
    <section>
      <div class="title-text">
        <h1 class="title-text1">영화처럼,</h1>
        <h1 class="title-text2">순간처럼</h1>
      </div>
    </section>

    <section>
      <div class="login-container">
        <form @submit.prevent="logIn" class="login-form">
          <div class="form-group">
            <label for="username">아이디</label>
            <input type="text" class="form-control id-input" id="username" v-model="credentials.username" placeholder="아이디를 입력해주세요." />
          </div>

          <div class="form-group">
            <label for="password">비밀번호</label>
            <input type="password" class="form-control pw-input" id="password" v-model="credentials.password" placeholder="비밀번호를 입력해주세요." />
          </div>

          <button type="submit" class="login-btn">로그인</button>
        </form>

        <div class="join-textbox">
          <p>혹시, 계정이 없으신가요?</p>
          <RouterLink to="/signup">회원가입</RouterLink>
        </div>
      </div>
    </section>

    <img src="@/assets/logo-img.svg" alt="메인 캐릭터" class="main-img" />
  </main>
</template>

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

<style scoped>
.login-main {
  padding: 30px 150px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  justify-content: center;
  position: relative;
  box-sizing: border-box;
  overflow: hidden;
  min-height: 100vh;
}

.main-img {
  position: absolute;
  bottom: -80px;
  right: -100px;
  width: 500px;
  z-index: 1;
}

.title-text {
  max-width: 300px;
  font-size: 50px;
  margin-bottom: 40px;
}

.title-text1 {
  text-align: left;
  font-weight: bold;
}

.title-text2 {
  text-align: right;
  font-weight: bold;
}

.login-container {
  display: flex;
  flex-direction: column;
  padding: 40px 100px 20px;
  margin-left: 40px;
  max-width: 600px;
  box-sizing: border-box;
  gap: 20px;
  background-color: #efefef;
  border-radius: 10px;
  position: relative;
  z-index: 2;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-size: 20px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.id-input,
.pw-input {
  margin-top: 20px;
  box-sizing: border-box;
  width: 100%;
  padding: 15px;
  border-radius: 5px;
  font-size: 15px;
  border: none;
  background-color: white;
}

.id-input:focus,
.pw-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(128, 128, 128, 0.2);
}

.login-btn {
  color: white;
  background-color: grey;
  border: none;
  border-radius: 5px;
  padding: 15px 0px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-btn:hover {
  background-color: #666;
}

.join-textbox {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  color: #666;
}

.join-textbox a {
  text-decoration: none;
  color: gray;
  font-weight: 500;
}

@media (max-width: 768px) {
  .login-main {
    padding: 20px;
  }

  .login-container {
    padding: 30px 20px;
    margin-left: 0;
  }

  .title-text {
    font-size: 40px;
    margin-bottom: 30px;
  }

  .main-img {
    width: 300px;
    right: -50px;
  }
}
</style>
