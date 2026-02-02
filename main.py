from enum import StrEnum
from pathlib import Path

import typer

from hymt_translator import HYMTTranslator
from nllb_translator import NLLBTranslator
from terms import load_terms
from translator import Language

app = typer.Typer()


class ModelType(StrEnum):
    NLLB = "nllb"
    HYMT = "hymt"


DEFAULT_MODEL_DIRS = {
    ModelType.NLLB: Path("./models/nllb-200-distilled-600M"),
    ModelType.HYMT: Path("./models/HY-MT1.5-1.8B"),
}


@app.command()
def main(
    model_type: ModelType = typer.Option(
        ModelType.NLLB,
        "--model",
        help="번역 모델 선택 (nllb, hymt)",
    ),
    model_dir: Path | None = typer.Option(
        None,
        "--model-dir",
        "-m",
        help="모델 저장 디렉토리 (미지정 시 모델별 기본값 사용)",
    ),
    terms_file: Path = typer.Option(
        Path("./terms.txt"),
        "--terms",
        "-t",
        help="전문 용어 파일 경로",
    ),
):
    if model_dir is None:
        model_dir = DEFAULT_MODEL_DIRS[model_type]

    if model_type == ModelType.NLLB:
        translator = NLLBTranslator(model_dir)
    else:
        translator = HYMTTranslator(model_dir)

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
        ko_protected, en_raw, english = translator.translate_with_terms(
            korean_input, Language.KOREAN, Language.ENGLISH, terms
        )
        en_protected, ko_raw, korean_back = translator.translate_with_terms(
            english, Language.ENGLISH, Language.KOREAN, terms
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
