from dataclasses import dataclass
from pathlib import Path

import typer
import uvicorn
from litestar import Litestar, post
from litestar.di import Provide

from hymt_translator import HYMTTranslator
from nllb_translator import NLLBTranslator
from terms import load_terms
from translator import Language, TermProtectedTranslator, Translator

LANG_MAP = {
    "ko": Language.KOREAN,
    "en": Language.ENGLISH,
}


@dataclass
class TranslateRequest:
    text: str
    src_lang: str
    tgt_lang: str


@dataclass
class TranslateResponse:
    translated: str


@post("/translate")
async def translate_handler(
    data: TranslateRequest,
    translator: Translator,
) -> TranslateResponse:
    src = LANG_MAP[data.src_lang]
    tgt = LANG_MAP[data.tgt_lang]
    result = translator.translate(data.text, src, tgt)
    return TranslateResponse(translated=result)


def create_app(
    model_type: str,
    model_dir: Path,
    terms_file: Path,
) -> Litestar:
    if model_type == "nllb":
        base = NLLBTranslator(model_dir)
    else:
        base = HYMTTranslator(model_dir)

    terms = load_terms(terms_file)
    translator = TermProtectedTranslator(base, terms)

    return Litestar(
        route_handlers=[translate_handler],
        dependencies={"translator": Provide(lambda: translator, sync_to_thread=False)},
    )


cli = typer.Typer()


@cli.command()
def serve(
    model_type: str = typer.Option("nllb", "--model", help="번역 모델 (nllb, hymt)"),
    model_dir: Path | None = typer.Option(
        None, "--model-dir", "-m", help="모델 디렉토리"
    ),
    terms_file: Path = typer.Option(
        Path("./terms.txt"), "--terms", "-t", help="용어 파일"
    ),
    host: str = typer.Option("0.0.0.0", "--host", help="바인드 호스트"),
    port: int = typer.Option(8000, "--port", "-p", help="포트"),
):
    default_dirs = {
        "nllb": Path("./models/nllb-200-distilled-600M"),
        "hymt": Path("./models/HY-MT1.5-1.8B"),
    }
    if model_dir is None:
        model_dir = default_dirs[model_type]

    app = create_app(model_type, model_dir, terms_file)
    uvicorn.run(app, host=host, port=port)


def run():
    cli()
