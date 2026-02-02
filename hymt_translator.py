import logging
from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer

from translator import Language, Translator

# HY-MT 모델은 커스텀 YaRN RoPE 파라미터를 사용하지만, transformers의
# 'dynamic' rope_type은 이를 인식하지 못함. 모델은 자체 구현으로 처리하므로 무시.
logging.getLogger("transformers.modeling_rope_utils").setLevel(logging.ERROR)

MODEL_ID = "tencent/HY-MT1.5-1.8B"

LANGUAGE_NAMES = {
    Language.KOREAN: "Korean",
    Language.ENGLISH: "English",
}


class HYMTTranslator(Translator):
    """tencent/HY-MT1.5-1.8B 기반 번역기"""

    def __init__(self, model_dir: Path):
        if model_dir.exists():
            print("로컬 모델 로딩 중...", flush=True)
            self._tokenizer = AutoTokenizer.from_pretrained(
                model_dir, local_files_only=True
            )
            self._model = AutoModelForCausalLM.from_pretrained(
                model_dir,
                local_files_only=True,
                device_map="auto",
                tie_word_embeddings=False,
            )
        else:
            print("모델 다운로드 중... (최초 1회)", flush=True)
            self._tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
            self._model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID,
                device_map="auto",
                tie_word_embeddings=False,
            )

            print("모델 로컬 저장 중...", flush=True)
            model_dir.mkdir(parents=True, exist_ok=True)
            self._tokenizer.save_pretrained(model_dir)
            self._model.save_pretrained(model_dir)

    def translate(self, text: str, src_lang: Language, tgt_lang: Language) -> str:
        tgt_name = LANGUAGE_NAMES[tgt_lang]
        prompt = (
            f"Translate the following segment into {tgt_name}, "
            f"without additional explanation.\n\n{text}"
        )

        messages = [{"role": "user", "content": prompt}]
        tokenized = self._tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True,
        )

        input_ids = tokenized["input_ids"].to(self._model.device)
        attention_mask = tokenized["attention_mask"].to(self._model.device)

        outputs = self._model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=256,
            top_k=20,
            top_p=0.6,
            repetition_penalty=1.05,
            temperature=0.7,
            do_sample=True,
        )

        # 입력 토큰 이후의 출력만 디코딩
        generated_tokens = outputs[0][input_ids.shape[1] :]
        return self._tokenizer.decode(generated_tokens, skip_special_tokens=True)
