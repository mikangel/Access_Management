# 🏢 IT 운영실 출입관리시스템

![image](https://github.com/user-attachments/assets/43079b10-cd76-4c5f-9cdd-30268d5b85ea)


## 📖 프로젝트 소개

IT회사 운영실(서버실)의 외부인 출입을 체계적으로 관리하기 위한 웹 기반 출입관리 시스템입니다. 
외부 업체 직원의 출입 등록부터 퇴실까지의 전 과정을 디지털화하여 관리할 수 있으며, 
법적 요구사항과 보안 정책을 준수한 출입 기록을 유지합니다.

## ✨ 주요 기능

### 🚪 출입 관리
- **출입 등록**: 외부인과 입회자(농협 직원) 정보 등록
- **퇴실 등록**: 현재 출입중인 인원 조회 및 퇴실 처리
- **실시간 현황**: 현재 출입중인 인원 실시간 확인

### 🎯 NFC 카드 리더 연동
- **자동 입력**: 사원증 태그로 입회자/확인자 정보 자동 입력
- **작업계획서 연동**: 담당자별 작업계획서 자동 조회
- **Python 서비스**: 별도 NFC 서비스와 연동

### ✍️ 디지털 서명
- **Canvas 기반**: 마우스/터치로 실시간 서명 입력
- **다중 서명**: 출입자, 입회자, 책임자 서명 관리
- **이미지 저장**: PNG 형태로 서명 데이터 저장

### 📋 작업계획서 관리
- **자동 조회**: 입회자별 작업계획서 필터링
- **직접 입력**: 수동 작업계획서 번호 입력 지원
- **사유 연동**: 작업계획서 사유 자동 입력 옵션

### 👨‍💼 책임자 확인
- **일괄 처리**: 다중 선택으로 여러 출입기록 동시 확인
- **확인 현황**: 미확인/확인완료 상태 관리
- **NFC 연동**: 확인자 정보 자동 입력

### 🔒 개인정보 보호
- **이름 마스킹**: 화면 표시 시 중간 글자 * 처리
- **접근 제어**: 설정 페이지 비밀번호 보호
- **데이터 암호화**: 백업 파일 암호화 지원

### 💾 데이터 관리
- **MySQL 백업**: 수동/자동 데이터베이스 백업
- **보고서 인쇄**: 기간별 출입기록 보고서 생성
- **Excel 내보내기**: 출입 데이터 Excel 형태 백업

## 🛠 기술 스택

### Frontend
- **HTML5/CSS3**: 반응형 웹 인터페이스
- **JavaScript (ES6+)**: 클라이언트 사이드 로직
- **Bootstrap 5.3**: UI 컴포넌트 및 반응형 디자인
- **Canvas API**: 디지털 서명 구현
- **Font Awesome**: 아이콘 시스템

### Backend
- **Node.js**: 서버 사이드 런타임
- **Express.js**: 웹 프레임워크
- **MySQL**: 출입 기록 데이터베이스
- **JSON**: 데이터 교환 형식

### NFC Integration
- **Python**: NFC 카드 리더 서비스
- **HTTP API**: Python-Node.js 간 통신
- **WebAPI**: 브라우저-Python 서비스 연동

## 📁 프로젝트 구조

```
access-management-system/
├── public/
│   ├── index.html          # 메인 페이지
│   ├── register.html       # 출입 등록
│   ├── exit.html          # 퇴실 등록
│   ├── verify.html        # 책임자 확인
│   ├── settings.html      # 설정 및 인쇄
│   └── assets/            # 이미지 리소스
├── server.js              # Node.js 서버
├── simple_nfc_web.py      # NFC 서비스 (Python)
├── package.json           # 의존성 관리
└── README.md             # 프로젝트 문서
```

## 🚀 설치 및 실행

### 1. 환경 요구사항
- **Node.js** 14.0 이상
- **MySQL** 5.7 이상
- **Python** 3.7 이상 (NFC 기능 사용 시)
- **NFC 리더기** (선택사항)

### 2. 저장소 클론
```bash
git clone https://github.com/your-username/access-management-system.git
cd access-management-system
```

### 3. 의존성 설치
```bash
# Node.js 의존성 설치
npm install

# Python 의존성 설치 (NFC 기능 사용 시)
pip install -r requirements.txt
```

### 4. 데이터베이스 설정
```sql
-- MySQL 데이터베이스 생성
CREATE DATABASE access_log CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 테이블 생성 (server.js에서 자동 생성됨)
CREATE TABLE entry_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    company VARCHAR(255),
    reason TEXT,
    plan_number VARCHAR(255),
    entry_sign TEXT,
    witness_name VARCHAR(255),
    witness_team VARCHAR(255),
    witness_sign TEXT,
    entry_time DATETIME,
    exit_time DATETIME NULL,
    exit_sign TEXT NULL,
    checker_name VARCHAR(255) NULL,
    checker_team VARCHAR(255) NULL,
    checker_sign TEXT NULL
);
```

### 5. 서버 실행
```bash
# Node.js 서버 실행
node server.js

# NFC 서비스 실행 (별도 터미널)
python simple_nfc_web.py
```

### 6. 접속
브라우저에서 `http://localhost:3000` 접속

## 📖 사용법

### 1️⃣ 출입 등록
1. **출입자 정보 입력**: 이름, 소속, 서명
2. **입회자 정보 입력**: NFC 카드 태그 또는 수동 입력
3. **작업계획서 선택**: 자동 조회 또는 직접 입력
4. **출입사유 입력**: 직접 입력 또는 작업계획서 연동
5. **등록 완료**: 서명 확인 후 등록

### 2️⃣ 퇴실 등록
1. **현황 조회**: 현재 출입중인 인원 확인
2. **인원 선택**: 퇴실할 인원 선택
3. **서명 입력**: 퇴실자 서명 입력
4. **퇴실 처리**: 퇴실 시간 자동 기록

### 3️⃣ 책임자 확인
1. **기록 조회**: 날짜별 출입 기록 조회
2. **항목 선택**: 확인할 기록 다중 선택
3. **확인자 정보**: NFC 태그 또는 수동 입력
4. **일괄 확인**: 선택된 기록 일괄 확인 처리

### 4️⃣ 설정 및 백업
1. **DB 백업**: MySQL 데이터베이스 백업
2. **보고서 생성**: 기간별 출입 기록 보고서
3. **비밀번호 변경**: 설정 페이지 접근 권한 관리

## 🔐 보안 기능

- **접근 제어**: 설정 페이지 비밀번호 보호
- **개인정보 마스킹**: 화면 표시 시 이름 중간 글자 * 처리
- **데이터 암호화**: 백업 파일 암호화 지원
- **세션 관리**: sessionStorage 기반 임시 권한 관리

## 🔧 설정

### 기본 설정값
- **서버 포트**: 3000
- **NFC 서비스 포트**: 8080
- **기본 비밀번호**: 1234 (최초 설정 후 변경 권장)

### 커스터마이징
- **직원 팀 목록**: `register.html`, `verify.html`에서 수정
- **작업계획서 데이터**: `register.html`의 `WORKPLAN_SAMPLE_DATA`
- **NFC 직원 데이터**: `simple_nfc_web.py`의 `EMPLOYEE_DB`

## 📱 반응형 지원

- **데스크톱**: 전체 기능 지원
- **태블릿**: 터치 서명 지원
- **모바일**: 기본 기능 지원 (일부 제한)

## 🤝 기여 방법

1. Fork 프로젝트
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원 및 문의

- **이슈 리포트**: [GitHub Issues](https://github.com/your-username/access-management-system/issues)
- **기능 요청**: [GitHub Discussions](https://github.com/your-username/access-management-system/discussions)

## 🔄 버전 히스토리

- **v1.0.0** (2025-06): 초기 릴리스
  - 기본 출입관리 기능
  - NFC 카드 리더 연동
  - 디지털 서명 시스템
  - MySQL 백업 기능

---

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!
