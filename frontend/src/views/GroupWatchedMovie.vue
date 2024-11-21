<template>
  <div>
    <h1>GroupWatchedMovie</h1>
    <button @click="goArticleCreate">게시글 생성</button>

    <div v-if="movie">
      <!-- 백드롭 이미지 섹션 (전체 폭) -->
      <div class="position-relative movie-backdrop mb-4">
        <img :src="`https://image.tmdb.org/t/p/original/${movie.backdrop_path}`" :alt="movie.title" class="w-100" />
        <!-- 영화 정보 오버레이 -->
        <div class="movie-info-overlay">
          <div class="container">
            <h1 class="display-4 text-white mb-2">{{ movie.title }}</h1>
            <div class="d-flex flex-wrap align-items-center text-white gap-3">
              <span>{{ new Date(movie.release_date).getFullYear() }}</span>
              <span>•</span>
              <span>{{ movie.runtime }}분</span>
              <span>•</span>
              <span>{{ movie.genres?.map((genre) => genre.name).join(", ") }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
</script>

<style lang="scss" scoped></style>
