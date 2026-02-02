import re
from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_ID = "facebook/nllb-200-distilled-600M"
LOCAL_MODEL_DIR = Path(__file__).parent / "models" / "nllb-200-distilled-600M"
TERMS_FILE = Path(__file__).parent / "terms.txt"


def load_terms() -> list[str]:
    if not TERMS_FILE.exists():
        return []
    terms = []
    for line in TERMS_FILE.read_text().splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    # 긴 용어부터 매칭하도록 정렬
    return sorted(terms, key=len, reverse=True)


def protect_terms(text: str, terms: list[str]) -> tuple[str, dict[str, str]]:
    """전문 용어를 플레이스홀더로 교체"""
    placeholders = {}
    protected = text
    idx = 0
    for term in terms:
        # 대소문자 무시 매칭
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        matches = pattern.findall(protected)
        for match in matches:
            if match not in placeholders.values():
                placeholder = f"<T{idx}>"
                placeholders[placeholder] = match
                protected = protected.replace(match, placeholder, 1)
                idx += 1
    return protected, placeholders


def restore_terms(text: str, placeholders: dict[str, str]) -> str:
    """플레이스홀더를 원래 용어로 복원"""
    restored = text
    for placeholder, term in placeholders.items():
        restored = restored.replace(placeholder, term)
    return restored


def load_model():
    if LOCAL_MODEL_DIR.exists():
        print("로컬 모델 로딩 중...", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_DIR, local_files_only=True)
        model = AutoModelForSeq2SeqLM.from_pretrained(
            LOCAL_MODEL_DIR, local_files_only=True, device_map="auto"
        )
    else:
        print("모델 다운로드 중... (최초 1회)", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID, device_map="auto")

        print("모델 로컬 저장 중...", flush=True)
        LOCAL_MODEL_DIR.mkdir(parents=True, exist_ok=True)
        tokenizer.save_pretrained(LOCAL_MODEL_DIR)
        model.save_pretrained(LOCAL_MODEL_DIR)

    return model, tokenizer


def translate(model, tokenizer, text: str, src_lang: str, tgt_lang: str) -> str:
    tokenizer.src_lang = src_lang
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    generated = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
        max_new_tokens=128,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3,
    )

    return tokenizer.decode(generated[0], skip_special_tokens=True)


def translate_with_terms(
    model, tokenizer, text: str, src_lang: str, tgt_lang: str, terms: list[str]
) -> str:
    """전문 용어를 보호하며 번역"""
    protected, placeholders = protect_terms(text, terms)
    translated = translate(model, tokenizer, protected, src_lang, tgt_lang)
    restored = restore_terms(translated, placeholders)
    return restored


def main():
    model, tokenizer = load_model()
    print("모델 로딩 완료!\n")

    terms = load_terms()
    if terms:
        print(f"용어집 로드됨: {len(terms)}개 용어")
        print(f"  예: {terms[:5]}")
    else:
        print("용어집 없음 (terms.txt 파일을 생성하면 전문 용어 보호 가능)")
    print()

    while True:
        korean_input = input("한국어 입력 (종료: q): ").strip()
        if korean_input.lower() == "q":
            break

        if not korean_input:
            continue

        print("\n번역 중...")
        english = translate_with_terms(
            model, tokenizer, korean_input, "kor_Hang", "eng_Latn", terms
        )
        korean_back = translate_with_terms(
            model, tokenizer, english, "eng_Latn", "kor_Hang", terms
        )

        print("\n" + "=" * 50)
        print(f"원본 한국어: {korean_input}")
        print(f"번역된 영어: {english}")
        print(f"재번역 한국어: {korean_back}")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
