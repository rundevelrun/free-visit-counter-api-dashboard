# 방문자 카운터

아름다운 대시보드와 API가 있는 웹사이트용 경량 방문자 카운터입니다.

![방문자 카운터 대시보드](https://via.placeholder.com/800x400?text=방문자+카운터+대시보드)

## 📋 목차

- [기능](#기능)
- [빠른 시작](#빠른-시작)
- [NPM 패키지](#npm-패키지)
- [API 문서](#api-문서)
- [설치](#설치)
- [배포](#배포)
- [설정](#설정)
- [다국어 지원](#다국어-지원)
- [기여하기](#기여하기)
- [라이선스](#라이선스)

## ✨ 기능

- **실시간 추적**: 정확한 카운팅과 중복 방지 기능으로 실시간으로 방문자를 추적합니다
- **반응형 대시보드**: 반응형 대시보드로 모든 기기에서 방문자 통계를 확인할 수 있습니다
- **쉬운 통합**: 간단한 API로 모든 웹사이트나 애플리케이션에 쉽게 통합할 수 있습니다
- **다중 웹사이트**: 단일 계정으로 여러 도메인의 방문자를 추적합니다
- **다국어 지원**: 영어, 한국어, 일본어로 제공됩니다
- **다크/라이트 테마**: 편안한 보기를 위해 다크 및 라이트 테마 간 전환이 가능합니다
- **중복 방지**: 20분 TTL이 있는 Redis를 사용하여 동일한 방문자를 여러 번 카운트하지 않습니다
- **시간대 지원**: 방문자의 시간대를 기준으로 "오늘"을 계산합니다
- **NPM 패키지**: JavaScript 프레임워크와 쉽게 통합할 수 있는 공식 NPM 패키지

## 🚀 빠른 시작

### 1. 웹사이트에 이 스크립트 추가하기

<code-block language="html">
<script>
(function() {
  const domain = encodeURIComponent(window.location.hostname);
  const timezone = encodeURIComponent(Intl.DateTimeFormat().resolvedOptions().timeZone);
  
  fetch('https://visitor.6developer.com/visit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ domain, timezone })
  })
  .then(response => response.json())
  .then(data => {
    console.log('방문자 수:', data);
    // 페이지에 카운트를 표시할 수 있습니다
    if (document.getElementById('visitor-count')) {
      document.getElementById('visitor-count').textContent = data.totalCount;
    }
  })
  .catch(error => console.error('오류:', error));
})();
</script>
</code-block>

### 2. 대시보드 보기

`https://visitor.6developer.com/login`으로 이동하여 도메인을 입력하면 방문자 통계를 볼 수 있습니다.

## 📦 NPM 패키지

공식 NPM 패키지를 사용하여 JavaScript 프레임워크와 쉽게 통합할 수 있습니다:

<code-block language="bash">
npm install @rundevelrun/free-visitor-counter
</code-block>

### React에서 사용하기

<code-block language="jsx">
import { VisitorCounter } from '@rundevelrun/free-visitor-counter';

function App() {
  return (
    <div>
      <h1>내 웹사이트</h1>
      <VisitorCounter />
    </div>
  );
}
</code-block>

### JavaScript에서 사용하기

<code-block language="javascript">
import { trackVisit, displayCounter } from '@rundevelrun/free-visitor-counter';

// 방문 기록
trackVisit().then(data => {
  console.log('방문자 수:', data);
});

// "visitor-counter" ID를 가진 요소에 카운터 표시
displayCounter('visitor-counter');
</code-block>

자세한 내용은 [GitHub 저장소](https://github.com/rundevelrun/free-visitor-counter)를 참조하세요.

## 📊 API 문서

### 기본 URL

<code-block>
https://visitor.6developer.com
</code-block>

### 방문 기록하기

<code-block>
POST /visit
</code-block>

**요청 본문:**

<code-block language="json">
{
  "domain": "example.com",
  "timezone": "Asia/Seoul" // 선택 사항, 기본값은 UTC
}
</code-block>

**응답:**

<code-block language="json">
{
  "dashboardUrl": "https://visitor.6developer.com/dashboard?domain=example.com",
  "totalCount": 42,
  "todayCount": 5
}
</code-block>

### 방문 통계 가져오기

<code-block>
GET /visit?domain=example.com
</code-block>

**응답:**

<code-block language="json">
{
  "dashboardUrl": "https://visitor.6developer.com/dashboard?domain=example.com",
  "totalCount": 42,
  "todayCount": 5
}
</code-block>

자세한 내용은 [API 문서](https://visitor.6developer.com/api-docs)를 참조하세요.

## 🛠️ 설치

### 필수 조건

- Python 3.9+
- PostgreSQL
- Redis

### 설정

1. 저장소 복제

<code-block language="bash">
git clone https://github.com/rundevelrun/visitor-counter.git
cd visitor-counter
</code-block>

2. 가상 환경 생성

<code-block language="bash">
python -m venv venv
source venv/bin/activate  # Windows에서는: venv\Scripts\activate
</code-block>

3. 의존성 설치

<code-block language="bash">
pip install -r requirements.txt
</code-block>

4. 환경 변수 설정

프로젝트 루트에 `.env` 파일 생성:

<code-block>
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost/visitor_counter
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
</code-block>

5. 데이터베이스 초기화

<code-block language="bash">
flask db init
flask db migrate -m "초기 마이그레이션"
flask db upgrade
</code-block>

6. 애플리케이션 실행

<code-block language="bash">
flask run
</code-block>

## 🚀 배포

### VPS에 배포하기

1. 서버에 Python 환경 설정
2. PostgreSQL 및 Redis 설치
3. 저장소 복제 및 설치 단계 수행
4. 프로덕션 WSGI 서버(Gunicorn, uWSGI) 설정
5. Nginx를 리버스 프록시로 구성

Nginx 구성 예시:

<code-block language="nginx">
server {
    listen 80;
    server_name visitor.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
</code-block>

### 공유 호스팅에 배포하기

1. 호스팅 제공업체에 파일 업로드
2. 지원되는 경우 가상 환경 설정
3. Apache용 `.htaccess` 파일 또는 다른 서버용 동등한 파일 구성
4. 특정 경로로 `passenger_wsgi.py` 파일 업데이트

## ⚙️ 설정

### 환경 변수

- `SECRET_KEY`: Flask 세션용 비밀 키
- `DATABASE_URL`: PostgreSQL 연결 문자열
- `REDIS_HOST`: Redis 호스트
- `REDIS_PORT`: Redis 포트
- `REDIS_PASSWORD`: Redis 비밀번호(필요한 경우)
- `REDIS_DB`: Redis 데이터베이스 번호

### 데이터베이스 마이그레이션

모델 변경 후 새 마이그레이션 생성:

<code-block language="bash">
flask db migrate -m "변경 사항 설명"
flask db upgrade
</code-block>

## 🌐 다국어 지원

이 애플리케이션은 영어, 한국어, 일본어를 지원합니다. 새 언어를 추가하려면:

1. 메시지 추출:

<code-block language="bash">
pybabel extract -F babel.cfg -o messages.pot .
</code-block>

2. 새 번역 생성:

<code-block language="bash">
pybabel init -i messages.pot -d translations -l [언어_코드]
</code-block>

3. `translations/[언어_코드]/LC_MESSAGES/`에 있는 `.po` 파일 편집

4. 번역 컴파일:

<code-block language="bash">
pybabel compile -d translations
</code-block>

## 🤝 기여하기

기여는 환영합니다! Pull Request를 제출해 주세요.

1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경 사항 커밋 (`git commit -m '놀라운 기능 추가'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 열기

## 📄 라이선스

이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다 - 자세한 내용은 LICENSE 파일을 참조하세요.