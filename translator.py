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

    def translate_with_terms(
        self, text: str, src_lang: Language, tgt_lang: Language, terms: list[str]
    ) -> tuple[str, str, str]:
        protected, placeholders = protect_terms(text, terms)
        translated = self.translate(protected, src_lang, tgt_lang)
        restored = restore_terms(translated, placeholders)
        return protected, translated, restored
