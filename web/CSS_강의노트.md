# CSS 레이아웃 & 반응형 디자인 강의 노트

## 📌 1. Position (위치 지정)

> 요소를 어디에, 무엇을 기준으로 배치할지 정하는 속성

### Position 속성 값 비교표

| 속성값 | 설명 | 노멀 플로우 | 기준점 | 주요 용도 |
|--------|------|-------------|--------|-----------|
| `static` | 기본값 | ✅ 따름 | 없음 (이동 불가) | 일반 배치 |
| `relative` | 상대 위치 | ✅ 따름 | 자기 원래 위치 | 미세 조정, absolute 기준점 |
| `absolute` | 절대 위치 | ❌ 벗어남 | position 있는 가장 가까운 조상 | 팝업, 배지, 오버레이 |
| `fixed` | 고정 위치 | ❌ 벗어남 | 뷰포트(화면) | 고정 헤더, 플로팅 버튼 |

### 위치 조정 속성

| 속성 | 설명 |
|------|------|
| `top` | 위에서부터 거리 |
| `bottom` | 아래에서부터 거리 |
| `left` | 왼쪽에서부터 거리 |
| `right` | 오른쪽에서부터 거리 |

### 코드 예제

```html
<!-- position.html -->
<!DOCTYPE html>
<html>
<head>
  <style>
    .container {
      width: 200px;
      height: 200px;
      border: 3px solid black;
      margin-bottom: 40px;
      position: relative; /* absolute의 기준점 */
    }
    .box {
      width: 100px;
      height: 100px;
      background-color: orange;
      position: absolute;
      top: 30px;
      left: 30px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="box"></div>
  </div>
</body>
</html>
```

---

## 📌 2. Flexbox (플렉스 박스)

> 한 방향(가로/세로)으로 요소들을 유연하게 배치하는 1차원 레이아웃 시스템

### 핵심 개념

| 개념 | 설명 |
|------|------|
| Flex Container | `display: flex`가 적용된 부모 요소 |
| Flex Item | 플렉스 컨테이너 안의 자식 요소들 |
| 주축 (Main Axis) | 기본적으로 가로 방향 |
| 교차축 (Cross Axis) | 주축에 수직인 방향 |

### Flex Container 속성

| 속성 | 값 | 설명 |
|------|-----|------|
| `display` | `flex` | 플렉스 컨테이너로 지정 |
| `flex-direction` | `row` | 가로 배치 (기본값) |
| | `column` | 세로 배치 |
| | `row-reverse` | 가로 역방향 |
| | `column-reverse` | 세로 역방향 |
| `justify-content` | `flex-start` | 주축 시작점 정렬 |
| | `flex-end` | 주축 끝점 정렬 |
| | `center` | 주축 중앙 정렬 |
| | `space-between` | 양끝 정렬, 균등 간격 |
| | `space-around` | 균등 간격 (양끝 포함) |
| `align-items` | `flex-start` | 교차축 시작점 정렬 |
| | `flex-end` | 교차축 끝점 정렬 |
| | `center` | 교차축 중앙 정렬 |
| `gap` | `10px` 등 | 아이템 간 간격 |

### 정렬 방향 요약

```
┌─────────────────────────────────────────┐
│  flex-direction: row (기본)             │
│  ────────────────────────────►          │
│  주축: 가로  /  교차축: 세로            │
│                                         │
│  justify-content → 가로 정렬            │
│  align-items     → 세로 정렬            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  flex-direction: column                 │
│  │                                      │
│  │  주축: 세로  /  교차축: 가로         │
│  ▼                                      │
│  justify-content → 세로 정렬            │
│  align-items     → 가로 정렬            │
└─────────────────────────────────────────┘
```

### 코드 예제

```html
<!-- flex.html -->
<!DOCTYPE html>
<html>
<head>
  <style>
    .container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      background-color: orange;
      height: 400px;
    }
    .item {
      width: 80px;
      height: 80px;
      background-color: skyblue;
      border: 1px solid black;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="item">A</div>
    <div class="item">B</div>
    <div class="item">C</div>
  </div>
</body>
</html>
```

### 🎮 연습 게임
- **Flexbox Froggy**: https://flexboxfroggy.com/#ko

---

## 📌 3. 반응형 디자인

> 디바이스 화면 크기에 따라 레이아웃과 스타일이 자동으로 변하는 디자인

### 상대 단위 비교표

| 단위 | 기준 | 예시 | 설명 |
|------|------|------|------|
| `%` | 부모 요소 | `width: 50%` | 부모 너비의 50% |
| `vw` | 뷰포트 너비 | `width: 100vw` | 화면 너비의 100% |
| `vh` | 뷰포트 높이 | `height: 100vh` | 화면 높이의 100% |
| `rem` | 루트 폰트 크기 | `font-size: 2rem` | 루트(html) 폰트의 2배 |
| `em` | 부모 폰트 크기 | `font-size: 1.5em` | 부모 폰트의 1.5배 |

### 미디어 쿼리 문법

```css
@media (조건) {
  /* 조건 만족 시 적용될 스타일 */
}
```

| 조건 | 설명 |
|------|------|
| `max-width: 600px` | 화면 너비 600px 이하일 때 |
| `min-width: 768px` | 화면 너비 768px 이상일 때 |

### 코드 예제

```html
<!-- media_query.html -->
<!DOCTYPE html>
<html>
<head>
  <style>
    .container {
      display: flex;
      gap: 10px;
    }
    .box {
      flex: 1;
      height: 100px;
      background-color: skyblue;
      border: 1px solid black;
    }
    
    /* 화면 너비 500px 이하일 때 */
    @media (max-width: 500px) {
      .container {
        flex-direction: column;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="box">A</div>
    <div class="box">B</div>
    <div class="box">C</div>
  </div>
</body>
</html>
```

---

## 📌 4. 네비게이션 바 만들기

### 구조

```
nav.navbar
├── div.navbar-logo (로고 + 링크)
├── ul.navbar-menu (메뉴 리스트)
│   ├── li > a (About)
│   ├── li > a (Resume)
│   └── li > a (Gallery)
└── ul.navbar-icons (아이콘 리스트)
    ├── li > i (GitHub)
    └── li > i (LinkedIn)
```

### 주요 CSS 속성

| 선택자 | 속성 | 값 | 설명 |
|--------|------|-----|------|
| `.navbar` | `display` | `flex` | 가로 배치 |
| | `justify-content` | `space-between` | 양끝 정렬 |
| | `align-items` | `center` | 세로 중앙 정렬 |
| | `padding` | `8px` | 내부 여백 |
| `.navbar-menu` | `list-style` | `none` | 점 제거 |
| | `display` | `flex` | 메뉴 가로 배치 |
| `.navbar-menu li:hover` | `background-color` | `white` | 호버 효과 |
| | `border-radius` | `8px` | 둥근 모서리 |

### 반응형 네비게이션 (모바일)

```css
@media (max-width: 600px) {
  .navbar {
    flex-direction: column; /* 세로 배치 */
  }
  .navbar-menu {
    flex-direction: column;
    width: 100%;
  }
  .navbar-icons {
    display: none; /* 아이콘 숨김 */
  }
}
```

---

## 📌 5. 팁 & 참고 자료

### 자주 쓰는 리셋 CSS

```css
body {
  margin: 0;
}
a {
  text-decoration: none;
  color: black;
}
ul {
  list-style: none;
  padding: 0;
}
```

### 가운데 정렬 꿀팁

```css
/* 가장 간단한 중앙 정렬 */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

### 참고 사이트

| 사이트 | 용도 |
|--------|------|
| [MDN Web Docs](https://developer.mozilla.org) | CSS/HTML 공식 문서 |
| [Flexbox Froggy](https://flexboxfroggy.com/#ko) | Flexbox 연습 게임 |
| [CSS Diner](https://flukeout.github.io/) | CSS 선택자 연습 게임 |
| [Font Awesome](https://fontawesome.com/) | 아이콘 라이브러리 |
