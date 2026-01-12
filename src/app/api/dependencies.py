import spacy
from spacy import Language

_SPACY_MODEL: Language | None = None


def _load_spacy_model(model_name: str = "en_core_web_sm") -> Language:
    try:
        return spacy.load(model_name)
    except OSError as e:
        raise OSError(
            f"spaCy model '{model_name}' not found. "
            f"Please install it with: python -m spacy download {model_name}"
        ) from e


def get_spacy_model(model_name: str = "en_core_web_sm") -> Language:
    global _SPACY_MODEL
    if _SPACY_MODEL is None:
        _SPACY_MODEL = _load_spacy_model(model_name)
    return _SPACY_MODEL
