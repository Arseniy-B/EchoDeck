import pytest
from pathlib import Path
from src.templates.read import read_templates


@pytest.fixture
def temp_dir(tmp_path: Path):
    (tmp_path / "login.txt").write_text("Hello {name}!", encoding="utf-8")
    (tmp_path / "register.TXT").write_text("Welcome {name}, code: {code}", encoding="utf-8")
    (tmp_path / "ignore.me").write_text("Не должен попасть", encoding="utf-8")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "hidden.txt").write_text("Скрытый", encoding="utf-8")
    
    return tmp_path


def test_read_templates_basic(temp_dir):
    templates = read_templates(temp_dir)
    
    assert len(templates) == 2
    assert "login" in templates
    assert "register" in templates
    assert templates["login"] == "Hello {name}!"
    assert templates["register"] == "Welcome {name}, code: {code}"


def test_read_templates_empty_dir(tmp_path):
    templates = read_templates(tmp_path)
    assert templates == {}


def test_read_templates_no_txt_files(tmp_path):
    (tmp_path / "image.png").write_bytes(b"fake")
    (tmp_path / "data.json").write_text("{}", encoding="utf-8")
    
    templates = read_templates(tmp_path)
    assert templates == {}


def test_read_templates_case_insensitive(temp_dir):
    templates = read_templates(temp_dir)
    assert "register" in templates  

def test_read_templates_encoding(tmp_path):
    special_text = "Привет, {name}! Код: {code}"
    (tmp_path / "russian.txt").write_text(special_text, encoding="utf-8")
    
    templates = read_templates(tmp_path)
    assert templates["russian"] == special_text
