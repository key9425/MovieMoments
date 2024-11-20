<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="signUp">
      <label for="name">
        <p>이름</p>
      </label>
      <input type="text" id="name" v-model.trim="name" placeholder="홍길동" />
      <br />

      <label for="email">
        <p>이메일</p>
      </label>
      <input type="text" id="email" v-model.trim="email" placeholder="example@example.com" />
      <br />

      <label for="username">
        <p>아이디</p>
      </label>
      <input type="text" id="username" v-model.trim="username" placeholder="아이디를 입력해주세요." />
      <p>한글/영문/숫자 10자까지</p>
      <br />

      <label for="password1">
        <p>비밀번호</p>
      </label>
      <input type="password" id="password1" v-model.trim="password1" placeholder="비밀번호를 입력해주세요." />
      <p>영문/숫자/특수문자 조합 8자 이상</p>
      <br />

      <label for="password2">
        <p>비밀번호 확인</p>
      </label>
      <input type="password" id="password2" v-model.trim="password2" placeholder="비밀번호를 한 번 더 입력해주세요." />
      <br />

      <input type="submit" value="회원가입" />
    </form>
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
  const payload = {
    name: name.value,
    email: email.value,
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  };
  store.signUp(payload);
};
</script>

<style></style>
