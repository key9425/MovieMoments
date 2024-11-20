<template>
  <div>
    <h1>영화처럼, 순간처럼</h1>
  </div>

  <section>
    <form @submit.prevent="logIn">
      <label for="username">
        <p>아이디</p>
        <input type="text" id="username" name="username" v-model.trim="username" placeholder="아이디를 입력해주세요." />
      </label>

      <label for="password">
        <p>비밀번호</p>
        <input type="password" id="password" name="password" v-model.trim="password" placeholder="비밀번호를 입력해주세요" class="pw-input" />
      </label>
      <br />
      <input type="submit" value="logIn" />
    </form>
  </section>

  <div>
    <p>혹시, 계정이 없으신가요?</p>
  </div>
  <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { RouterLink } from "vue-router";

const username = ref(null);
const password = ref(null);

const store = useCounterStore();

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};
</script>

<style></style>
