# 영화 그룹 기록 서비스 : 영화처럼, 순간처럼


## 1. 프로젝트 소개
### 프로젝트 내용
- 가입한 회원을 대상을 대상으로 한 영화 추천, 정보 제공 서비스
- 영화메이트(그룹)들과 함께 본 영화의 추억을 기록하는 서비스

### 기술 스택 & Tools
- Backend
<div align="center">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
 <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=SQLite&logoColor=white">
</div>

- Frontend
<div align="center">
<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
<img src="https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white">
<img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">
</div>

- Tools
피그마, 노션, Gitlab, dbdiagram.io

### 개발 기간
- 2024.11.18 ~ 2024.11.27 (10일)

### 팀명 
- CoDream

### 팀원
- 이송희 (FRONTEND)
- 김은영 (BACKEND)


## 2. 모델 설계 (dbdiagram.io)

- User
- Group
- Movie
- 




## 3. 주요 기능
### (메인) 그룹 영화 기록 서비스

### 로그인, 로그아웃, 회원가입
- django-rest-auth 라이브러리 활용
- user 커스텀 (name, profile_img 필드 추가)
- 비로그인 유저는 기능이 제한되어 로그인, 회원가입 페이지 외 접근 제한

### 영화 데이터 (최소 50개 이상)	
- TMDB API를 통해 영화 데이터 정보 DB 저장
- 영화 리스트 요청 후 id를 통해 상세 정보 재요청하여 상세 정보 저장

### 영화 목록 조회	
- 추천 영화 
  : TMDB API로부터 받아 저장한 50개 이상의 데이터로부터 랜덤으로 추천
  - 해당 DB는 사용자의 기록 서비스 이용에 따라 데이터 증가로 더 다양한 추천 가능
- 박스오피스
  : TMDB API 요청
- 현재상영작
  : TMDB API 요청
- 개봉예정작
  : TMDB API 요청

### 영화 상세 목록 조회	
- 영화 목록에서 영화 선택
- 영화 목록 조회에서 요청하여 받은 영화 id를 통해 TMDB API 상세 정보를 요청하여 제공
- 영화명, 개봉년도, 상영시간, 장르, 출연진, 사진 등 제공
- 영화 찜하기(좋아요) 기능

### 커뮤니티 게시글, 댓글
- 그룹을 만들어 함께 본 영화를 기록
- 타임라인 : 함께 본 날의 하루를 기록, 그룹에 속한 사람이라면 누구나 삭제 가능
- 한줄평 : 간단한 메모, 감상평, 명대사 등을 기록
- 게시글을 통해 사진 첨부 가능, 댓글 기록
- 갤러리 : 게시글에 첨부한 사진 모아보기

### 찜하기(좋아요)
- 영화 상세 페이지를 통해 좋아요 기능 구현
- User 모델과의 관계를 위해 LikeMovie 모델 설계하여 M:N 관계 설정 (Movie 모델에 저장하여도 되었으나 데이터 용량 고려)

### 프로필 조회
- 사용자 정보 조회, 수정, 삭제 
- 작성한 게시글 수, 팔로잉 수, 팔로워 수
- 최근 작성한 글
- 짬한 영화

### 팔로우
- User 모델에서 자신과 M:N 관계 설정
- 대칭적 관계가 아니므로  `symmetrical=False` 속성 설정
- 팔로우 상태 확인을 위해 DB에서 포함 여부를 확인하여 응답을 boolean으로 제공 -> 반응형 변수로 상태 변환 용이

### 영화 추천 알고리즘


### AI (추천 / 검색 서비스)




## 4. API 명세서
## 5. 일정 관리


## 6. 후기(느낀점, 어려웠던점, 배운점 등)
### 이송희 
### 김은영
- ERD Model 설계와 API 명세서의 중요성을 깨달음
- API 명세서를 기반으로 Frontend와 Backend의 역할을 확실히 구분하여 개발할 수 있음
- 그룹 관계 설정에 대한 어려움이 있었음
- 프로젝트 초반 Frontend와 Backend의 역할에 대해 구분이 명확하지 않아 어려움이 있었음
- User 모델을 커스텀
- 시리얼라이즈의 사용법
- url 주소 구분
- 예외 처리 부분


## 7. 추가 기능 예정
- 팔로워, 팔로잉한 사용자 확인
- 그룹 신청 요청(수락, 거절)
- 챌린지 서비스
- 비밀번호 수정
- 전체 공유 커뮤니티
- 오픈방
