from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_ID = "facebook/nllb-200-distilled-600M"
LOCAL_MODEL_DIR = Path(__file__).parent / "models" / "nllb-200-distilled-600M"


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


def main():
    model, tokenizer = load_model()
    print("모델 로딩 완료!\n")

    while True:
        korean_input = input("한국어 입력 (종료: q): ").strip()
        if korean_input.lower() == "q":
            break

        if not korean_input:
            continue

        print("\n번역 중...")
        english = translate(model, tokenizer, korean_input, "kor_Hang", "eng_Latn")
        korean_back = translate(model, tokenizer, english, "eng_Latn", "kor_Hang")

        print("\n" + "=" * 50)
        print(f"원본 한국어: {korean_input}")
        print(f"번역된 영어: {english}")
        print(f"재번역 한국어: {korean_back}")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
