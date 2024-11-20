import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
  const API_URL = "http://127.0.0.1:8000";
  const token = ref(null);
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
      url: `${API_URL}/accounts/signup1/`,
      data: {
        name,
        email,
        username,
        password1,
        password2,
      },
    })
      .then((response) => {
        // console.log(reponse);
        const password = password1;
        LoginView({ username, password });
      })
      .catch((error) => {
        console.log(error);
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
        token.value = response.data.key;
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
        token.value = null;
        router.push({ name: "LogInView" });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return { API_URL, token, isLogin, signUp, logIn, logOut };
});
