import pytest
from litestar import Litestar
from litestar.di import Provide
from litestar.testing import TestClient

from api import translate_handler
from translator import Language, Translator, TermProtectedTranslator


class MockTranslator(Translator):
    def translate(self, text: str, src_lang: Language, tgt_lang: Language) -> str:
        return f"[{tgt_lang}] {text}"


@pytest.fixture
def app() -> Litestar:
    translator = TermProtectedTranslator(MockTranslator(), [])
    return Litestar(
        route_handlers=[translate_handler],
        dependencies={"translator": Provide(lambda: translator, sync_to_thread=False)},
    )


@pytest.fixture
def client(app: Litestar) -> TestClient[Litestar]:
    return TestClient(app)


def test_translate_ko_to_en(client: TestClient[Litestar]):
    response = client.post(
        "/translate",
        json={"text": "안녕하세요", "src_lang": "ko", "tgt_lang": "en"},
    )

    assert response.status_code == 201
    assert response.json() == {"translated": "[eng_Latn] 안녕하세요"}


def test_translate_en_to_ko(client: TestClient[Litestar]):
    response = client.post(
        "/translate",
        json={"text": "hello", "src_lang": "en", "tgt_lang": "ko"},
    )

    assert response.status_code == 201
    assert response.json() == {"translated": "[kor_Hang] hello"}


def test_translate_missing_field(client: TestClient[Litestar]):
    response = client.post(
        "/translate",
        json={"text": "hello"},
    )

    assert response.status_code == 400


def test_translate_invalid_lang(client: TestClient[Litestar]):
    response = client.post(
        "/translate",
        json={"text": "hello", "src_lang": "xx", "tgt_lang": "en"},
    )

    assert response.status_code == 500
