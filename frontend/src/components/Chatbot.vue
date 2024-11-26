<!-- FloatingMovieChat.vue -->
<template>
  <!-- 플로팅 버튼 -->
  <transition name="fade">
    <button v-if="!isExpanded" @click="toggleChat" class="floating-button">
      <span class="button-icon">🎬</span>
    </button>
  </transition>

  <!-- 채팅창 -->
  <transition name="slide">
    <div v-if="isExpanded" class="floating-chat">
      <!-- 헤더 -->
      <div class="chat-header">
        <h3>AI 영화 추천</h3>
        <button class="close-button" @click="toggleChat">×</button>
      </div>

      <!-- 메인 컨텐츠 영역 -->
      <div class="chat-content">
        <!-- 선택 패널 토글 버튼 -->
        <div class="selection-toggle">
          <button @click="toggleSelectionPanel" class="toggle-button">
            {{ isSelectionPanelOpen ? "선택 패널 닫기 ▼" : "장르/분위기 선택 ▲" }}
          </button>
        </div>

        <!-- 선택 패널 -->
        <transition name="fade">
          <div v-if="isSelectionPanelOpen" class="selection-sections">
            <div class="selection-section">
              <h3 class="section-title">장르 선택</h3>
              <div class="chip-grid">
                <label v-for="genre in genres" :key="genre.id" class="chip" :class="{ selected: selectedGenres.includes(genre.id) }">
                  <input type="checkbox" :value="genre.id" v-model="selectedGenres" class="hidden" />
                  {{ genre.name }}
                </label>
              </div>
            </div>

            <div class="selection-section">
              <h3 class="section-title">분위기 선택</h3>
              <div class="chip-grid">
                <label v-for="(mood, id) in moods" :key="id" class="chip mood-chip" :class="{ selected: selectedMood === id }" @click="toggleMood(id)">
                  {{ mood.label }}
                </label>
              </div>
            </div>
          </div>
        </transition>

        <!-- 채팅 메시지 영역 -->
        <div class="chat-section" ref="chatContainer">
          <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
            <div class="message-content" v-if="message.type === 'bot' && message.movieInfo">
              <h4 class="movie-title">{{ message.movieInfo.title }}</h4>
              <div class="movie-meta">
                <span class="year">{{ message.movieInfo.year }}</span>
                <span class="genre">{{ message.movieInfo.genre }}</span>
              </div>
              <div class="mood-tag">분위기: {{ message.movieInfo.mood }}</div>
              <p class="recommendation-reason">{{ message.movieInfo.reason }}</p>
              <div class="watch-points">
                <h5>감상 포인트:</h5>
                <ul>
                  <li v-for="(point, idx) in message.movieInfo.points" :key="idx">
                    {{ point }}
                  </li>
                </ul>
              </div>
              <div class="similar-movies">
                <h5>비슷한 분위기의 추천작:</h5>
                <ul>
                  <li v-for="(movie, idx) in message.movieInfo.similar" :key="idx">
                    {{ movie }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="message-content" v-else>
              {{ message.text }}
            </div>
          </div>
          <div v-if="isLoading" class="message bot">
            <div class="loading-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 입력 영역 -->
      <div class="input-section">
        <input v-model="userInput" @keyup.enter="sendMessage" :placeholder="inputPlaceholder" :disabled="isLoading" />
        <button @click="sendMessage" :disabled="!canSendMessage">
          {{ isLoading ? "처리중..." : "전송" }}
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed } from "vue";
import axios from "axios";

// 플로팅 채팅 상태
const isExpanded = ref(false);
const isSelectionPanelOpen = ref(false);

// 기존 상태 관리
const messages = ref([]);
const userInput = ref("");
const selectedGenres = ref([]);
const selectedMood = ref("");
const isLoading = ref(false);

// 토글 함수들
const toggleChat = () => {
  isExpanded.value = !isExpanded.value;
};

const toggleMood = (moodId) => {
  // 이미 선택된 분위기를 다시 클릭하면 선택 해제
  if (selectedMood.value === moodId) {
    selectedMood.value = "";
  } else {
    selectedMood.value = moodId;
  }
};

const toggleSelectionPanel = () => {
  isSelectionPanelOpen.value = !isSelectionPanelOpen.value;
};

// 장르 및 분위기 데이터
const genres = [
  { id: "action", name: "액션" },
  { id: "drama", name: "드라마" },
  { id: "romance", name: "로맨스" },
  { id: "thriller", name: "스릴러" },
  { id: "comedy", name: "코미디" },
  { id: "horror", name: "공포" },
  { id: "scifi", name: "SF" },
  { id: "fantasy", name: "판타지" },
];

const moods = {
  uplifting: {
    label: "희망적",
    description: "긍정적이고 희망적인 감동을 주는 분위기",
    keywords: "희망, 성장, 극복, 영감",
  },
  melancholic: {
    label: "감성적",
    description: "깊이 있는 감성과 여운을 주는 분위기",
    keywords: "그리움, 상실, 치유, 성찰",
  },
  thrilling: {
    label: "긴장감",
    description: "긴장감과 흥분을 주는 강렬한 분위기",
    keywords: "서스펜스, 액션, 반전",
  },
  heartwarming: {
    label: "따뜻한",
    description: "따뜻한 위로와 공감을 주는 분위기",
    keywords: "가족, 우정, 사랑, 치유",
  },
  contemplative: {
    label: "사색적",
    description: "깊은 사색과 통찰을 주는 분위기",
    keywords: "철학적, 실존적, 심리적",
  },
};

// API 클라이언트 설정
const apiClient = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
  },
  timeout: 60000,
});

// 계산된 속성
const canSendMessage = computed(() => userInput.value.trim() && !isLoading.value);
const inputPlaceholder = computed(() => "영화 추천을 요청해보세요...");

// 메시지 전송 관련 함수들
const generatePrompt = (userMessage) => {
  let prompt = "";
  if (selectedGenres.value.length > 0) {
    const selectedGenreNames = selectedGenres.value.map((id) => genres.find((g) => g.id === id)?.name).filter(Boolean);
    prompt += `선택된 장르: ${selectedGenreNames.join(", ")}\n`;
  }
  if (selectedMood.value) {
    const mood = moods[selectedMood.value];
    prompt += `원하는 분위기: ${mood.description}\n`;
    prompt += `분위기 키워드: ${mood.keywords}\n`;
  }
  prompt += `${userMessage}\n\n`;
  prompt += `다음 형식으로 추천해주세요:
  제목: [영화 제목(영문 제목)]
  개봉년도: [년도]
  장르: [주요 장르, 부가 장르]
  분위기: [주요 감정선과 분위기]
  추천이유: [3-4문장으로 설명]
  감상 포인트:
  - [핵심 포인트 1]
  - [핵심 포인트 2]
  비슷한 분위기의 추천작:
  - [영화 1]
  - [영화 2]`;
  return prompt;
};

const parseResponse = (response) => {
  try {
    const lines = response.split("\n");
    let movieInfo = {};
    let currentSection = "";
    lines.forEach((line) => {
      line = line.trim();
      if (line.startsWith("제목:")) movieInfo.title = line.replace("제목:", "").trim();
      else if (line.startsWith("개봉년도:")) movieInfo.year = line.replace("개봉년도:", "").trim();
      else if (line.startsWith("장르:")) movieInfo.genre = line.replace("장르:", "").trim();
      else if (line.startsWith("분위기:")) movieInfo.mood = line.replace("분위기:", "").trim();
      else if (line.startsWith("추천이유:")) movieInfo.reason = line.replace("추천이유:", "").trim();
      else if (line.startsWith("감상 포인트:")) {
        currentSection = "points";
        movieInfo.points = [];
      } else if (line.startsWith("비슷한 분위기의 추천작:")) {
        currentSection = "similar";
        movieInfo.similar = [];
      } else if (line.startsWith("-")) {
        const content = line.replace("-", "").trim();
        if (currentSection === "points") movieInfo.points.push(content);
        else if (currentSection === "similar") movieInfo.similar.push(content);
      }
    });
    return movieInfo;
  } catch (error) {
    console.error("응답 파싱 에러:", error);
    return null;
  }
};

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return;

  messages.value.push({
    type: "user",
    text: userInput.value,
  });

  isLoading.value = true;

  try {
    const prompt = generatePrompt(userInput.value);
    const { data } = await apiClient.post("/chat/completions", {
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: "당신은 전문 영화 큐레이터입니다. 사용자의 요청에 따라 영화를 추천하고, 추천한 영화에 대해 자세한 설명을 제공합니다.",
        },
        {
          role: "user",
          content: prompt,
        },
      ],
      temperature: 0.7,
      max_tokens: 1000,
      top_p: 1,
    });

    const responseContent = data.choices[0]?.message?.content;
    if (!responseContent) {
      throw new Error("Invalid API response structure");
    }

    const movieInfo = parseResponse(responseContent.trim());
    if (!movieInfo) {
      throw new Error("Failed to parse movie info");
    }

    messages.value.push({
      type: "bot",
      movieInfo,
    });

    userInput.value = "";
  } catch (error) {
    console.error("Error details:", error.response?.data || error.message || error);
    messages.value.push({
      type: "bot",
      text: "죄송합니다. 오류가 발생했습니다. 다시 시도해주세요.",
    });
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 기본 레이아웃 */
.floating-chat {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 400px;
  height: 80vh;
  max-height: 800px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

/* 플로팅 버튼 */
.floating-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 30px;
  background-color: #2196f3;
  border: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: transform 0.2s;
}

.floating-button:hover {
  transform: scale(1.1);
}

.button-icon {
  font-size: 24px;
}

/* 헤더 */
.chat-header {
  padding: 15px;
  background-color: #2196f3;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 12px 12px 0 0;
}

.chat-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0 5px;
}

/* 메인 컨텐츠 영역 */
.chat-content {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  position: relative;
  height: calc(100% - 130px); /* 헤더와 입력창 높이 제외 */
}

/* 선택 패널 토글 버튼 */
.selection-toggle {
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.toggle-button {
  width: 100%;
  padding: 8px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  color: #666;
  transition: background-color 0.2s;
}

.toggle-button:hover {
  background-color: #eee;
}

/* 선택 패널 */
.selection-sections {
  background: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.selection-section {
  margin-bottom: 10px;
}

.section-title {
  font-size: 0.9rem;
  margin-bottom: 8px;
  color: #666;
}

/* 칩 스타일 */
.chip-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.chip {
  padding: 4px 12px;
  border-radius: 16px;
  background-color: #f0f0f0;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s ease;
}

.chip:hover {
  background-color: #e0e0e0;
}

.chip.selected {
  background-color: #2196f3;
  color: white;
}

.mood-chip.selected {
  background-color: #4caf50;
}

/* 채팅 섹션 */
.chat-section {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* 메시지 스타일 */
.message {
  max-width: 85%;
  margin-bottom: 10px;
  animation: fadeIn 0.3s ease;
}

.message.user {
  margin-left: auto;
  background-color: #e3f2fd;
  padding: 10px;
  border-radius: 12px 12px 0 12px;
}

.message.bot {
  margin-right: auto;
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 12px 12px 12px 0;
}

/* 영화 정보 스타일 */
.movie-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1976d2;
  margin-bottom: 6px;
}

.movie-meta {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 6px;
}

.mood-tag {
  display: inline-block;
  padding: 3px 8px;
  background-color: #e8f5e9;
  color: #2e7d32;
  border-radius: 4px;
  font-size: 0.85rem;
  margin-bottom: 8px;
}

.recommendation-reason {
  margin-bottom: 10px;
  line-height: 1.4;
  font-size: 0.95rem;
}

.watch-points,
.similar-movies {
  margin-top: 8px;
}

.watch-points h5,
.similar-movies h5 {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 6px;
  color: #2c3e50;
}

.watch-points ul,
.similar-movies ul {
  list-style: none;
  padding-left: 0;
}

.watch-points li,
.similar-movies li {
  padding-left: 16px;
  position: relative;
  margin-bottom: 4px;
  font-size: 0.9rem;
}

.watch-points li:before,
.similar-movies li:before {
  content: "•";
  position: absolute;
  left: 4px;
  color: #2196f3;
}

/* 입력 섹션 */
.input-section {
  position: sticky;
  bottom: 0;
  padding: 15px;
  background: white;
  border-top: 1px solid #eee;
  border-radius: 0 0 12px 12px;
  display: flex;
  gap: 8px;
  z-index: 2;
}

.input-section input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
}

.input-section button {
  padding: 10px 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.input-section button:hover {
  background-color: #1976d2;
}

.input-section button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 로딩 인디케이터 */
.loading-indicator {
  display: flex;
  gap: 4px;
  justify-content: center;
  padding: 8px;
}

.loading-indicator span {
  width: 6px;
  height: 6px;
  background-color: #2196f3;
  border-radius: 50%;
  animation: bounce 0.5s infinite alternate;
}

.loading-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}
.loading-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

/* 애니메이션 */
@keyframes bounce {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-6px);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 트랜지션 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* 모바일 반응형 */
@media (max-width: 480px) {
  .floating-chat {
    width: 100%;
    height: 100vh;
    bottom: 0;
    right: 0;
    border-radius: 0;
    max-height: none;
  }

  .chat-content {
    height: calc(100vh - 130px);
  }

  .input-section {
    border-radius: 0;
  }
}
</style>
