import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/views/LoginView.vue";
import SignUpForm from "@/components/SignUpForm.vue";
import SignUpSurvey from "@/components/SignUpSurvey.vue";
import HomeView from "@/views/HomeView.vue";
import MovieView from "@/views/MovieView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/signup1",
      name: "SignUpForm",
      component: SignUpForm,
    },
    {
      path: "/signup2",
      name: "SignUpSurvey",
      component: SignUpSurvey,
    },
    {
      path: "/",
      name: "LoginView",
      component: LoginView,
    },
    {
      path: "/home",
      name: "HomeView",
      component: HomeView,
    },
    {
      path: "/movie",
      name: "MovieView",
      component: MovieView,
    },
  ],
});

// [추가] 메인페이지 접근인데 로그인 상태 아니면 로그인 페이지로 보내기
export default router;
