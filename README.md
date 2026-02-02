# kek - 한영 번역기

저자원 환경에서 실행 가능한 한국어-영어 번역 시스템.

## 목표

- **저자원 실행**: 고성능 GPU 없이도 실행 가능
- **번역 특화**: 범용 LLM이 아닌 번역 전용 모델 사용
- **모델 크기 제한**: 5B 파라미터 이하 ([ADR-001](docs/adr/001-model-size-constraint.md))

## 실행

```bash
uv run main.py
```

## 현재 모델

`facebook/nllb-200-distilled-600M` (600M)

## 문서

- [대안 모델 목록](docs/alternative-models.md)
- [ADR-001: 모델 크기 제한](docs/adr/001-model-size-constraint.md)
