from abc import ABC, abstractmethod
from enum import StrEnum

from terms import protect_terms, restore_terms


class Language(StrEnum):
    KOREAN = "kor_Hang"
    ENGLISH = "eng_Latn"


class Translator(ABC):
    @abstractmethod
    def translate(self, text: str, src_lang: Language, tgt_lang: Language) -> str:
        pass


class TermProtectedTranslator(Translator):
    """용어 보호 기능을 추가하는 래퍼"""

    def __init__(self, translator: Translator, terms: list[str]):
        self._translator = translator
        self._terms = terms
        self.last_protected: str | None = None
        self.last_raw: str | None = None

    def translate(self, text: str, src_lang: Language, tgt_lang: Language) -> str:
        protected, placeholders = protect_terms(text, self._terms)
        self.last_protected = protected
        translated = self._translator.translate(protected, src_lang, tgt_lang)
        self.last_raw = translated
        return restore_terms(translated, placeholders)
