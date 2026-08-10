# 🚀 Squard Goalz API Server

FastAPI와 PostgreSQL(Neon DB)을 이용해 구축한 로그인 및 유저 관리 API 서버입니다. 
비밀번호는 AES-256-GCM 알고리즘으로 안전하게 양방향 암호화되어 저장됩니다.

---

## 💻 1. 개발 환경 세팅 및 실행 방법 (Windows 기준)

프로젝트를 처음 다운로드했거나 다른 컴퓨터에서 실행할 때 아래 순서대로 진행하세요.

### ① 가상 환경 생성 및 활성화
터미널을 열고 프로젝트 폴더로 이동한 뒤, 독립적인 파이썬 가상 환경을 만들고 활성화합니다.
```bash
python -m venv venv
.\venv\Scripts\activate
```
*(성공하면 터미널 입력줄 맨 앞에 `(venv)`가 표시됩니다.)*

### ② 필수 패키지 설치
API 서버 구동과 DB 연결, 암호화에 필요한 패키지들을 한 번에 설치합니다.
```bash
pip install "fastapi[standard]" psycopg2-binary python-dotenv cryptography
```

### ③ 환경 변수 (.env) 설정
프로젝트 최상단(`login.py`와 같은 위치)에 `.env` 파일을 만들고 아래 정보를 입력합니다. 
**(🚨 주의: .env 파일은 보안을 위해 절대 깃허브에 올리지 마세요!)**

```env
DB_HOST=본인의_DB_호스트_주소
DB_NAME=sq_goalz
DB_USER=DB_아이디
DB_PASSWORD=DB_비밀번호
AES_SECRET_KEY=정확히_32글자로_된_나만의_영문숫자_비밀키
```

### ④ 서버 실행
세팅이 모두 완료되었다면 아래 명령어로 서버를 켭니다.
```bash
fastapi dev login.py
```
* **API 테스트 및 문서 확인:** 브라우저에서 `http://127.0.0.1:8000/docs` 로 접속하세요.

---

## ☁️ 2. 깃허브(GitHub) 배포 및 코드 업데이트 방법

코드를 수정하고 나서 깃허브에 안전하게 백업(배포)하고 싶을 때, 터미널(`venv` 활성화 상태)에서 아래 3단계를 순서대로 입력합니다.

### 1단계: 변경된 파일 모두 담기
```bash
git add .
```

### 2단계: 작업 내역 메모 남기기
```bash
git commit -m "여기에 무슨 작업을 했는지 간단히 적어주세요 (예: 로그인 기능 추가)"
```

### 3단계: 깃허브 서버로 쏘아 올리기
```bash
git push
```
*(만약 충돌 에러가 난다면 `git push --force` 를 사용해 내 컴퓨터 기준으로 강제 덮어쓰기를 할 수 있습니다.)*