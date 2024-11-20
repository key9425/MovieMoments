import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
  const API_URL = "http://127.0.0.1:8000";
  // localstorage에서 토큰을 가져와 초기값으로 설정
  // const token = ref(null);
  const token = ref(localStorage.getItem("token"));
  const isLogin = computed(() => {
    if (token.value === null) {
      return false;
    } else {
      return true;
    }
  });
  const router = useRouter();

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
        const password = password1;
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
        // 로그인 성공하면 localstorage에 토큰 저장
        localStorage.setItem("token", response.data.key);
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
    })
      .then((response) => {
        console.log(response.data);
        console.log("로그아웃 성공");
        token.value = null;
        // 로그아웃하면 localstorage에서 토큰 제거
        localStorage.removeItem("token");
        router.push({ name: "LogInView" });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return { API_URL, token, isLogin, signUp, logIn, logOut };
});
