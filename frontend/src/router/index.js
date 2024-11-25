import { createRouter, createWebHistory } from "vue-router";
import LogInView from "@/views/LoginView.vue";
import SignUpView from "@/views/SignUpView.vue";
import HomeView from "@/views/HomeView.vue";
import MovieView from "@/views/MovieView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import ProfileView from "@/views/ProfileView.vue";
import GroupDetailView from "@/views/GroupDetailView.vue";
import GroupWatchedMovie from "@/views/GroupWatchedMovie.vue";
import ArticleCreate from "@/components/ArticleModal.vue";
import Timeline from "@/components/GroupWatchedMovie/Timeline.vue";
import OneLineReview from "@/components/GroupWatchedMovie/OneLineReview.vue";
import Article from "@/components/GroupWatchedMovie/Article.vue";
import Gallery from "@/components/GroupWatchedMovie/Gallery.vue";
import { useCounterStore } from "@/stores/counter";
import { storeToRefs } from "pinia";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "LogInView",
      component: LogInView,
      // Navbar 숨기기
      meta: { hideNavbar: true },
    },
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
      meta: { hideNavbar: true },
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
      path: "/group/:group_id",
      name: "GroupDetailView",
      component: GroupDetailView,
    },
    {
      path: "/group/:group_id/:group_movie_id",
      name: "GroupWatchedMovie",
      component: GroupWatchedMovie,
      children: [
        {
          path: "",
          name: "MovieTimeline",
          component: Timeline,
        },
        {
          path: "reviews",
          name: "MovieReviews",
          component: OneLineReview,
        },
        {
          path: "articles",
          name: "MovieArticles",
          component: Article,
        },
        {
          path: "gallery",
          name: "MovieGallery",
          component: Gallery,
        },
      ],
    },
    {
      path: "/article/create/:group_movie_id",
      name: "ArticleCreate",
      component: ArticleCreate,
    },
  ],
});

// [추가] 메인페이지 접근인데 로그인 상태 아니면 로그인 페이지 보내기
router.beforeEach((to, from) => {
  const store = useCounterStore();
  const { isLogin } = storeToRefs(store);

  if (to.name !== "LogInView" && to.name !== "SignUpView" && !isLogin.value) {
    window.alert("로그인이 필요합니다.");
    return { name: "LogInView" };
  } else if ((to.name === "LogInView" || to.name === "SignUpView") && isLogin.value) {
    window.alert("로그인이 되어있습니다.");
    return { name: from.name || "HomeView" };
  }
});

export default router;
