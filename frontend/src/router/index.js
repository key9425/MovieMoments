import { createRouter, createWebHistory } from "vue-router";
import LogInView from "@/views/LogInView.vue";
import SignUpView from "@/views/SignUpView.vue";
import HomeView from "@/views/HomeView.vue";
import MovieView from "@/views/MovieView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/",
      name: "LogInView",
      component: LogInView,
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
    {
      path: "/movie/:movieId",
      name: "MovieDetailView",
      component: MovieDetailView,
    },
  ],
});

// [추가] 메인페이지 접근인데 로그인 상태 아니면 로그인 페이지로 보내기
router.beforeEach((to, from) => {
  if (to.name === "ArticleView" && !store.isLogin) {
    window.alert("로그인이 필요합니다.");
    return { name: "LogInView" };
  }
});

export default router;
