# SAFE API

숙명여자대학교 AGI연구팀의 **S.A.F.E. 산행안전 AI 플랫폼** 백엔드 서버입니다.
아이나비시스템즈와 연동하여 등산 중 수집되는 생체 데이터, 등산로 정보, POI 정보, 등반 이력 등을 처리하고 AI 분석 결과를 반환합니다.

## 프로젝트 개요

본 프로젝트는 FastAPI 기반의 AI 백엔드 서버로, 아이나비 서버와 REST API 방식으로 통신합니다.

주요 역할은 다음과 같습니다.

* 워치 생체 데이터 수신
* 등산로 및 POI 정보 수신
* 등반 이력 데이터 수신
* AI 분석 결과 생성
* 아이나비 서버로 결과 데이터 전송
* PostgreSQL 기반 데이터 저장

## 기술 스택

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* httpx
* Uvicorn

## 프로젝트 구조

```text
safe_api/
├── main.py
├── database.py
├── utils.py
├── models/
│   ├── __init__.py
│   └── biometric.py
├── schemas/
│   ├── __init__.py
│   ├── biometric.py
│   ├── common.py
│   ├── history.py
│   ├── poi.py
│   ├── result.py
│   └── trail.py
├── routers/
│   ├── __init__.py
│   ├── biometric.py
│   ├── history.py
│   ├── poi.py
│   └── trail.py
└── services/
    ├── __init__.py
    ├── inavi_client.py
    ├── result.py
    └── ml/
```

## 디렉토리 설명

### `main.py`

FastAPI 애플리케이션의 진입점입니다.
라우터 등록, 서버 실행, API 문서 설정 등을 담당합니다.

### `database.py`

PostgreSQL 데이터베이스 연결 설정을 담당합니다.
SQLAlchemy 엔진, 세션 생성, DB 의존성 주입 함수 등을 포함합니다.

### `models/`

데이터베이스 테이블 구조를 정의하는 SQLAlchemy 모델 파일을 관리합니다.

예시:

* `biometric.py` : 워치 생체 데이터 저장용 DB 모델

### `schemas/`

API 요청 및 응답 데이터 형식을 정의하는 Pydantic 스키마를 관리합니다.

주요 파일:

* `biometric.py` : DTO-1, 워치 생체 데이터 스키마
* `trail.py` : DTO-2, 등산로 데이터 스키마
* `poi.py` : DTO-3, POI 데이터 스키마
* `history.py` : DTO-4, 등반 이력 데이터 스키마
* `result.py` : DTO-5, AI 분석 결과 반환 스키마
* `common.py` : 공통 응답 형식

### `routers/`

API 엔드포인트를 정의하는 라우터 파일을 관리합니다.

주요 파일:

* `biometric.py` : 생체 데이터 수신 API
* `trail.py` : 등산로 데이터 수신 API
* `poi.py` : POI 데이터 수신 API
* `history.py` : 등반 이력 데이터 수신 API

### `services/`

비즈니스 로직과 외부 서버 통신 로직을 관리합니다.

주요 파일:

* `result.py` : AI 분석 결과 생성 및 DTO-5 생성 로직
* `inavi_client.py` : 아이나비 서버 API 호출 전담 클라이언트
* `ml/` : 추후 AI/ML 모델 관련 코드 관리 디렉토리

## 현재 구현 상태

| DTO   | 설명        | 구현 상태                          |
| ----- | --------- | ------------------------------ |
| DTO-1 | 워치 생체 데이터 | 수신 및 DB 저장 구현                  |
| DTO-2 | 등산로 데이터   | 수신 엔드포인트 구현                    |
| DTO-3 | POI 데이터   | 수신 엔드포인트 구현                    |
| DTO-4 | 등반 이력 데이터 | 수신 엔드포인트 구현                    |
| DTO-5 | AI 분석 결과  | 더미 데이터 생성 및 아이나비 서버 POST 전송 구현 |

## API 실행 방법

가상환경 활성화 후 서버를 실행합니다.

```bash
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

서버 실행 후 Swagger 문서는 아래 경로에서 확인할 수 있습니다.

```text
http://서버IP:8000/docs
```

## 아이나비 서버 연동

`services/inavi_client.py`는 아이나비 서버와 실제 HTTP 통신을 담당합니다.

주요 역할:

* 아이나비 서버 health check 호출
* DTO-5 AI 결과 데이터 POST 전송
* 외부 API 호출 실패 시 예외 처리
