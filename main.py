import re
from pathlib import Path

import typer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_ID = "facebook/nllb-200-distilled-600M"

app = typer.Typer()


def load_terms(terms_file: Path) -> list[str]:
    if not terms_file.exists():
        return []
    terms = []
    for line in terms_file.read_text().splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    return sorted(terms, key=len, reverse=True)


def protect_terms(text: str, terms: list[str]) -> tuple[str, dict[str, str]]:
    placeholders = {}
    protected = text
    idx = 0
    for term in terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        matches = pattern.findall(protected)
        for match in matches:
            if match not in placeholders.values():
                placeholder = f"TERM{idx}"
                placeholders[placeholder] = match
                protected = protected.replace(match, placeholder, 1)
                idx += 1
    return protected, placeholders


def restore_terms(text: str, placeholders: dict[str, str]) -> str:
    restored = text
    for placeholder, term in placeholders.items():
        restored = restored.replace(placeholder, term)
    return restored


def load_model(model_dir: Path):
    if model_dir.exists():
        print("로컬 모델 로딩 중...", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_dir, local_files_only=True, device_map="auto"
        )
    else:
        print("모델 다운로드 중... (최초 1회)", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID, device_map="auto")

        print("모델 로컬 저장 중...", flush=True)
        model_dir.mkdir(parents=True, exist_ok=True)
        tokenizer.save_pretrained(model_dir)
        model.save_pretrained(model_dir)

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
) -> tuple[str, str, str]:
    protected, placeholders = protect_terms(text, terms)
    translated = translate(model, tokenizer, protected, src_lang, tgt_lang)
    restored = restore_terms(translated, placeholders)
    return protected, translated, restored


@app.command()
def main(
    model_dir: Path = typer.Option(
        Path("./models/nllb-200-distilled-600M"),
        "--model-dir",
        "-m",
        help="모델 저장 디렉토리",
    ),
    terms_file: Path = typer.Option(
        Path("./terms.txt"),
        "--terms",
        "-t",
        help="전문 용어 파일 경로",
    ),
):
    model, tokenizer = load_model(model_dir)
    print("모델 로딩 완료!\n")

    terms = load_terms(terms_file)
    if terms:
        print(f"용어집 로드됨: {len(terms)}개 용어")
        print(f"  예: {terms[:5]}")
    else:
        print(f"용어집 없음 ({terms_file} 파일을 생성하면 전문 용어 보호 가능)")
    print()

    while True:
        korean_input = input("한국어 입력 (종료: q): ").strip()
        if korean_input.lower() == "q":
            break

        if not korean_input:
            continue

        print("\n번역 중...")
        ko_protected, en_raw, english = translate_with_terms(
            model, tokenizer, korean_input, "kor_Hang", "eng_Latn", terms
        )
        en_protected, ko_raw, korean_back = translate_with_terms(
            model, tokenizer, english, "eng_Latn", "kor_Hang", terms
        )

        print("\n" + "=" * 50)
        print(f"원본 한국어: {korean_input}")
        print(f"  → 플레이스홀더: {ko_protected}")
        print(f"  → 번역 결과(raw): {en_raw}")
        print(f"번역된 영어: {english}")
        print(f"  → 플레이스홀더: {en_protected}")
        print(f"  → 번역 결과(raw): {ko_raw}")
        print(f"재번역 한국어: {korean_back}")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    app()
