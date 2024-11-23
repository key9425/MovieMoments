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

          // 에러 응답에서 첫 번째 에러 메시지를 추출
          if (error.response?.data) {
            const firstErrorKey = Object.keys(error.response.data)[0];
            const errorMessage = error.response.data[firstErrorKey];
            throw new Error(Array.isArray(errorMessage) ? errorMessage[0] : errorMessage);
          }
          throw new Error("회원가입 중 오류가 발생했습니다.");
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

          // 로그인 성공 시 추가적으로 프로필 정보 api를 통해 프로필 정보 외 기타 정보도 currentUser 정보로 저장
          axios({
            method: "get",
            url: `http://127.0.0.1:8000/api/v2/${response.data.user.id}/profile/`,
            headers: {
              Authorization: `Token ${response.data.key}`,
            },
          })
            .then((res) => {
              console.log(res.data);
              currentUser.value.id = res.data.id;
              currentUser.value.name = res.data.name;
              currentUser.value.username = res.data.username;
              currentUser.value.email = res.data.email;
              currentUser.value.profile_img = res.data.profile_img;
              currentUser.value.followers_count = res.data.followers_count;
              currentUser.value.followings_count = res.data.followings_count;
              currentUser.value.is_following = res.data.is_following;
            })
            .catch((err) => {
              console.log(err);
            });

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
