<template>
  
  <div>
    <h1>Home page</h1>
    <br />
    <form>
      <input type="text" placeholder="그룹검색" />
    </form>

    <button @click="goGroupCreate">그룹생성</button>
  </div>
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const groups = ref([]);


const groupCreate = function () {};


onMounted(() => {
  axios({
   method: 'get',
   url: 'http://127.0.0.1:8000/api/v1/groups/',
   headers: {
     Authorization: `Token ${store.token}`
   }
 })
 .then((res) => {
   console.log(res.data)
   groups.value = res.data
 })
 .catch((err) => {
   console.log(err)
 })
})
</script>

<style scoped></style>
