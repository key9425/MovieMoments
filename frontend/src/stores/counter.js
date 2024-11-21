import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore(
  "counter",
  () => {
    const API_URL = "http://127.0.0.1:8000";
    const router = useRouter();

    const token = ref(null);
    const currentUser = ref(null);
    const isLogin = computed(() => {
      if (token.value === null) {
        return false;
      } else {
        return true;
      }
    });

    // 회원가입 요청 액션
    // form이랑 survey 둘 다 받아서 처리해야 하는데 ,,,
    const signUp = function (payload) {
      const { name, email, username, password1, password2 } = payload;

      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          name,
          email,
          username,
          password1,
          password2,
        },
      })
        .then((response) => {
          console.log(response.data);
          console.log("회원가입 성공");
          router.push({ name: "LogInView" });
        })
        .catch((error) => {
          console.log(error);
          console.log("Error response:", error.response?.data);
          console.log("Error status:", error.response?.status);
        });
    };

    // 로그인 요청 액션
    const logIn = function (payload) {
      const { username, password } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((response) => {
          console.log(response.data);
          console.log("로그인 성공");
          token.value = response.data.key;
          currentUser.value = response.data.user;
          console.log(currentUser);
          router.push({ name: "HomeView" });
        })
        .catch((error) => {
          console.log(error);
        });
    };

    // 로그아웃
    const logOut = function () {
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
        // headers: {
        //   Authorization: `Token ${token.value}`
        // }
      })
        .then((response) => {
          console.log(response.data);
          console.log("로그아웃 성공");
          token.value = null;
          currentUser.value = null;
          router.push({ name: "LogInView" });
        })
        .catch((error) => {
          console.log(error);
        });
    };

    // 회원탈퇴
    const deleteAccount = function () {
      if (confirm("정말 탈퇴하시겠습니까?")) {
        router.push({ name: "LogInView" });
        axios({
          method: "delete",
          url: `${API_URL}/api/v2/delete/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        })
          .then((response) => {
            console.log(response.data);
            router.push({ name: "LogInView" });
            token.value = null;
            currentUser.value = null;
          })
          .catch((error) => {
            console.log(error);
          });
      }
    };

    return { API_URL, token, isLogin, signUp, logIn, logOut, currentUser, deleteAccount };
  },
  { persist: true }
);
