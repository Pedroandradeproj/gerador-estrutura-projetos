# Testes para o módulo analyzer.py
import pytest
from src.backend.analyzer import StructureAnalyzer



def test_analyzer():
    input_text = """
    /projeto/
    │── /pasta1/
    │   ├── arquivo1.txt
    │── /pasta2/
    │   ├── arquivo2.txt
    """
    analyzer = StructureAnalyzer(input_text)
    structure = analyzer.get_structure()
    assert len(structure) == 4
    assert structure[0] == {"type": "folder", "path": "projeto/pasta1"}
    assert structure[1] == {"type": "file", "path": "projeto/pasta1/arquivo1.txt"}