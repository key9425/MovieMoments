import { createRouter, createWebHistory } from "vue-router";
import LogInView from "@/views/LogInView.vue";
import SignUpView from "@/views/SignUpView.vue";
import HomeView from "@/views/HomeView.vue";
import MovieView from "@/views/MovieView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import ProfileView from "@/views/ProfileView.vue";
import GroupCreateView from "@/views/GroupCreateView.vue";
import GroupDetailView from "@/views/GroupDetailView.vue";
import GroupMovieCreateView from "@/views/GroupMovieCreateView.vue";
import GroupWatchedMovie from "@/views/GroupWatchedMovie.vue";
import ArticleCreate from "@/components/ArticleCreate.vue";
// import { useCounterStore } from "@/stores/counter";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
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
    {
      path: "/profile/:user_id",
      name: "ProfileView",
      component: ProfileView,
    },
    {
      path: "/group-create",
      name: "GroupCreateView",
      component: GroupCreateView,
    },
    {
      path: "/group/:group_id",
      name: "GroupDetailView",
      component: GroupDetailView,
    },
    {
      path: "/group-movie/create/:group_id",
      name: "GroupMovieCreateView",
      component: GroupMovieCreateView,
    },
    {
      path: "/group/:group_id/:group_movie_id",
      name: "GroupWatchedMovie",
      component: GroupWatchedMovie,
    },
    {
      path: "/article/create/:group_movie_id",
      name: "ArticleCreate",
      component: ArticleCreate,
    },
  ],
});

// [추가] 메인체이지 접근인데 로그인 상태 아니면 로그인 페이지 보내기
// router.beforeEach((to, from) => {
//   if (to.name === "ArticleView" && !storeToRefs.isLogin) {
//     window.alert("로그인이 필요합니다.");
//     return { name: "LogInView" };
//   }
// });
// router.beforeEach((to, from) => {
//   const store = useCounterStore()
//   // [추가] 로그인, 회원가입 외 로그인 상태 아니면 로그인 페이지로 보내기
//   if ((to.name === "LogInView" && to.name === "SignUpView") && !store.isLogin) {
//     window.alert("로그인이 필요합니다.");
//     return { name: "LogInView" };
//   }
//   // 로그인, 회원가입 페이지로 이동 시 로그인 되어 있다면 이전 페이지 유지
//   else if ((to.name === "LogInView" || to.name === "SignUpView") && store.islogin) {
//     window.alert("로그인이 되어있습니다.");
//     return { name: from.name || 'HomeView' };
//   }
// });

export default router;
