from enum import StrEnum
from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from terms import protect_terms, restore_terms

MODEL_ID = "facebook/nllb-200-distilled-600M"


class Language(StrEnum):
    KOREAN = "kor_Hang"
    ENGLISH = "eng_Latn"


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
