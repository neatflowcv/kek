from abc import ABC, abstractmethod
from enum import StrEnum
from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from terms import protect_terms, restore_terms

MODEL_ID = "facebook/nllb-200-distilled-600M"


class Language(StrEnum):
    KOREAN = "kor_Hang"
    ENGLISH = "eng_Latn"


class Translator(ABC):
    @abstractmethod
    def translate(self, text: str, src_lang: Language, tgt_lang: Language) -> str:
        pass

    def translate_with_terms(
        self, text: str, src_lang: Language, tgt_lang: Language, terms: list[str]
    ) -> tuple[str, str, str]:
        protected, placeholders = protect_terms(text, terms)
        translated = self.translate(protected, src_lang, tgt_lang)
        restored = restore_terms(translated, placeholders)
        return protected, translated, restored


class NLLBTranslator(Translator):
    def __init__(self, model_dir: Path):
        if model_dir.exists():
            print("로컬 모델 로딩 중...", flush=True)
            self._tokenizer = AutoTokenizer.from_pretrained(
                model_dir, local_files_only=True
            )
            self._model = AutoModelForSeq2SeqLM.from_pretrained(
                model_dir, local_files_only=True, device_map="auto"
            )
        else:
            print("모델 다운로드 중... (최초 1회)", flush=True)
            self._tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(
                MODEL_ID, device_map="auto"
            )

            print("모델 로컬 저장 중...", flush=True)
            model_dir.mkdir(parents=True, exist_ok=True)
            self._tokenizer.save_pretrained(model_dir)
            self._model.save_pretrained(model_dir)

    def translate(self, text: str, src_lang: Language, tgt_lang: Language) -> str:
        self._tokenizer.src_lang = src_lang
        inputs = self._tokenizer(text, return_tensors="pt").to(self._model.device)

        generated = self._model.generate(
            **inputs,
            forced_bos_token_id=self._tokenizer.convert_tokens_to_ids(tgt_lang),
            max_new_tokens=128,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
        )

        return self._tokenizer.decode(generated[0], skip_special_tokens=True)
