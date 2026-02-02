# 대안 번역 모델 (5B 이하)

현재 사용 중: `facebook/nllb-200-distilled-600M`

## 2025년 최신 모델

### Tencent HY-MT1.5 (2025.12)

WMT25 우승 모델 기반. 33개 언어 지원 (한국어 포함). 용어 개입, 문맥 번역, 포맷 번역 지원.

| 모델 | 크기 | 링크 |
|------|------|------|
| `tencent/HY-MT1.5-1.8B` | 1.8B | [HuggingFace](https://huggingface.co/tencent/HY-MT1.5-1.8B) |
| `tencent/HY-MT1.5-1.8B-GPTQ-Int4` | 1.8B (양자화) | [HuggingFace](https://huggingface.co/tencent/HY-MT1.5-1.8B-GPTQ-Int4) |

### GemmaX2 (Xiaomi, 2025.02)

Gemma2 기반 다국어 번역 모델. 28개 언어 지원 (한국어 포함).

| 모델 | 크기 | 라이선스 | 링크 |
|------|------|----------|------|
| `ModelSpace/GemmaX2-28-2B-v0.1` | 3B | Gemma | [HuggingFace](https://huggingface.co/ModelSpace/GemmaX2-28-2B-v0.1) |

### Sarvam Translate (2025.09)

인도 언어 특화 (22개 언어). 한국어 미지원.

| 모델 | 크기 | 라이선스 | 링크 |
|------|------|----------|------|
| `sarvamai/sarvam-translate` | 4B | GPL-3.0 | [HuggingFace](https://huggingface.co/sarvamai/sarvam-translate) |

---

## NLLB 시리즈 (Meta)

200개 언어 지원, NLLB (No Language Left Behind) 프로젝트.

| 모델 | 크기 | 라이선스 | 링크 |
|------|------|----------|------|
| `facebook/nllb-200-distilled-600M` | 600M | CC-BY-NC-4.0 | [HuggingFace](https://huggingface.co/facebook/nllb-200-distilled-600M) |
| `facebook/nllb-200-distilled-1.3B` | 1.3B | CC-BY-NC-4.0 | [HuggingFace](https://huggingface.co/facebook/nllb-200-distilled-1.3B) |
| `facebook/nllb-200-1.3B` | 1.3B | CC-BY-NC-4.0 | [HuggingFace](https://huggingface.co/facebook/nllb-200-1.3B) |
| `facebook/nllb-200-3.3B` | 3.3B | CC-BY-NC-4.0 | [HuggingFace](https://huggingface.co/facebook/nllb-200-3.3B) |

## M2M-100 (Meta)

100개 언어 지원, NLLB 이전 세대 모델. MIT 라이선스로 상업적 사용 가능.

| 모델 | 크기 | 라이선스 | 링크 |
|------|------|----------|------|
| `facebook/m2m100_418M` | 418M | MIT | [HuggingFace](https://huggingface.co/facebook/m2m100_418M) |
| `facebook/m2m100_1.2B` | 1.2B | MIT | [HuggingFace](https://huggingface.co/facebook/m2m100_1.2B) |

## SeamlessM4T (Meta)

음성+텍스트 통합 번역 모델. 96개 언어 텍스트 입출력 지원.

| 모델 | 크기 | 라이선스 | 출시 | 링크 |
|------|------|----------|------|------|
| `facebook/seamless-m4t-medium` | 1.2B | CC-BY-NC-4.0 | 2023.08 | [HuggingFace](https://huggingface.co/facebook/seamless-m4t-medium) |
| `facebook/seamless-m4t-large` | 2.3B | CC-BY-NC-4.0 | 2023.08 | [HuggingFace](https://huggingface.co/facebook/seamless-m4t-large) |
| `facebook/seamless-m4t-v2-large` | 2.3B | CC-BY-NC-4.0 | 2023.12 | [HuggingFace](https://huggingface.co/facebook/seamless-m4t-v2-large) |

**v2 추천**: `seamless-m4t-v2-large`는 v1 대비 품질과 속도 모두 개선됨. UnitY2 아키텍처 사용.

## MADLAD-400 (Google)

400개 이상 언어 지원, T5 기반. Apache 2.0 라이선스.

| 모델 | 크기 | 라이선스 | 링크 |
|------|------|----------|------|
| `google/madlad400-3b-mt` | 3B | Apache-2.0 | [HuggingFace](https://huggingface.co/google/madlad400-3b-mt) |

## Opus-MT (Helsinki-NLP)

언어쌍 특화 모델. 매우 가벼움.

| 모델 | 방향 | 라이선스 | 링크 |
|------|------|----------|------|
| `Helsinki-NLP/opus-mt-ko-en` | 한국어→영어 | Apache-2.0 | [HuggingFace](https://huggingface.co/Helsinki-NLP/opus-mt-ko-en) |

## 추천

| 목적 | 추천 모델 |
|------|----------|
| **최신 + 한국어** | `tencent/HY-MT1.5-1.8B` (2025.12, WMT25 우승) |
| 최신 + 가벼움 | `ModelSpace/GemmaX2-28-2B-v0.1` (2025.02, 3B) |
| 품질 향상 (현재 대비) | `nllb-200-distilled-1.3B` 또는 `nllb-200-3.3B` |
| 상업적 사용 | `m2m100_418M`, `m2m100_1.2B`, `madlad400-3b-mt` |
| 속도 중시 | `m2m100_418M`, `opus-mt-ko-en` |
| 최다 언어 지원 | `madlad400-3b-mt` (400+ 언어) |

---

## 참고: 5B 초과 최신 모델

아래 모델들은 5B 제한을 초과하지만, LLM 기반 번역의 최신 트렌드를 보여줌.

| 모델 | 크기 | 출시 | 특징 |
|------|------|------|------|
| `tencent/HY-MT1.5-7B` | 7B | 2025.12 | WMT25 우승, 한국어 지원 |
| `haoranxu/ALMA-7B-R` | 7B | 2024.01 | LLaMA 기반, GPT-4급 품질 |
| `Unbabel/TowerInstruct-7B-v0.2` | 7B | 2024.02 | 10개 언어 (한국어 미지원) |
