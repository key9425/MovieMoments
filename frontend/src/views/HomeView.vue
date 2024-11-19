<template>
  <div>
    <h1>Homp Page</h1>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import axios from 'axios';

onMounted(() => {
  createGroup()
})
const createGroup = function () {
  axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/api/v1/groups/',
    // post요청은 data, get요청은 parms
    data: {
      group_name: '싸피',
      description: '이것은 설명입니다.',
      category: '가족',
      members: [1, 2]
    },
    // headers: {
    //   Authorization: store.token
    // }
  })
    .then((res) => {
      console.log(res.data)
    })
    .catch((err) => {
      console.log(err)
    })
}

</script>

<style scoped>

</style>