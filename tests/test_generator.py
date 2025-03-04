# Testes para o módulo generator.py
import pytest
from src.backend.generator import CodeGenerator


def test_generator():
    structure = [
        {"type": "folder", "path": "projeto/pasta1"},
        {"type": "file", "path": "projeto/pasta1/arquivo1.txt"},
    ]
    generator = CodeGenerator(structure)
    code = generator.generate_code()
    assert "mkdir" in code
    assert "touch" in code