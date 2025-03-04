# Testes para o módulo validator.py
import pytest
from src.backend.validator import InputValidator


def test_validator():
    input_text = """
    /projeto/
    │── /pasta1/
    │   ├── arquivo1.txt
    """
    errors = InputValidator.validate(input_text)
    assert len(errors) == 0

    invalid_text = "projeto/pasta1/arquivo1*.txt"
    errors = InputValidator.validate(invalid_text)
    assert "Caracteres inválidos" in errors[0]