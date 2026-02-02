# Python REST API 프레임워크 비교 (2026)

번역 서비스를 REST API로 전환하고 Kubernetes에 배포하기 위한 프레임워크 조사.

## 요구사항

- 현대적인 설계
- 글로벌 변수 없는 명시적 의존성 주입(DI)
- ASGI 지원
- CPU 전용 (GPU 없음)

## 프레임워크 비교

| 프레임워크 | 버전 | 상태 | Python | DI 방식 | 글로벌 회피 |
|-----------|------|------|--------|---------|------------|
| **Litestar** | latest | Production | 3.9+ | `Provide()` 계층형 | `State` + 팩토리 |
| **BlackSheep** | 2.5.1 | Production | 3.10+ | 타입 기반 자동 | 팩토리 패턴 |
| **FastAPI** | latest | Production | 3.9+ | `Depends()` | 글로벌 일반적 |
| **Falcon** | 4.2.0 | Production | 3.9+ | 클래스 기반 수동 | 생성자 DI |
| **Robyn** | 0.76.0 | Alpha | 3.10+ | 내장 DI | Rust 런타임 |
| **Sanic** | 25.12.0 | Beta | 3.10+ | 앱 컨텍스트 | uvloop |

## 상세 분석

### Litestar

- **장점**
  - 명시적 `Provide()` DI (앱/라우터/컨트롤러/핸들러 레벨)
  - `State` 객체로 글로벌 변수 없이 상태 관리
  - 제너레이터 DI로 리소스 정리 (DB 연결 등)
  - OpenAPI 자동 생성
- **단점**
  - FastAPI 대비 커뮤니티 작음

```python
from litestar import Litestar, get
from litestar.di import Provide

def create_app() -> Litestar:
    translator = load_translator()
    return Litestar(
        route_handlers=[translate_handler],
        dependencies={"translator": Provide(lambda: translator)},
    )
```

### BlackSheep

- **장점**
  - ASP.NET Core 영감의 현대적 설계
  - 타입 기반 자동 DI
  - HTTP/2 클라이언트 내장
  - PyPy 지원
- **단점**
  - 문서가 FastAPI/Litestar 대비 부족

```python
from blacksheep import Application, get

app = Application()

@get("/")
async def home(translator: Translator) -> str:
    return translator.translate(...)
```

### FastAPI

- **장점**
  - 가장 큰 커뮤니티, 풍부한 문서
  - Pydantic 통합
  - OpenAPI 자동 생성
- **단점**
  - `Depends()`가 함수 시그니처에 혼재
  - 글로벌 `app` 패턴이 일반적

```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/")
def read_root(translator: Translator = Depends(get_translator)):
    return translator.translate(...)
```

### Falcon

- **장점**
  - 외부 의존성 제로
  - Cython 컴파일로 빠름
  - Production/Stable
- **단점**
  - 프레임워크 레벨 DI 없음 (수동)

```python
import falcon.asgi

class TranslateResource:
    def __init__(self, translator: Translator):
        self.translator = translator

    async def on_post(self, req, resp):
        ...
```

### Robyn

- **장점**
  - Rust 런타임 (TechEmpower 벤치마크 상위)
  - MCP/AI Agent 지원
- **단점**
  - **Alpha 상태** (프로덕션 주의)

### Sanic

- **장점**
  - uvloop 기반 고성능
  - CLI 지원
- **단점**
  - Beta 상태
  - DI가 명시적이지 않음

## 결론: Litestar 선택

1. 명시적 계층형 DI (`Provide()`)
2. `State` 객체로 글로벌 변수 완전 회피 가능
3. `create_app()` 팩토리 패턴 공식 지원
4. Production 안정성
5. OpenAPI 자동 생성

## 참고

- [Litestar 문서](https://docs.litestar.dev/)
- [Litestar DI](https://docs.litestar.dev/latest/usage/dependency-injection.html)
- [BlackSheep 문서](https://www.neoteroi.dev/blacksheep/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Falcon 문서](https://falcon.readthedocs.io/)
