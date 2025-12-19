from pathlib import Path
import os


def read_templates(template_dir: Path):

    templates_files: list[Path] = [
        template_dir / i for i in os.listdir(template_dir) if i.lower().endswith(".txt")
    ]

    TEMPLATES: dict[str, str] = {}

    for file in templates_files:
        TEMPLATES[file.stem] = file.read_text(encoding="utf-8")

    return TEMPLATES 
