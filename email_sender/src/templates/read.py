from pathlib import Path

templates_files: list[Path] = [
    Path(__file__).parent / "login_otp.txt",
    Path(__file__).parent / "register_otp.txt",
    Path(__file__).parent / "wellcome.txt",
]

TEMPLATES: dict[str, str] = {}

for file in templates_files:
    TEMPLATES[file.stem] = file.read_text(encoding="utf-8")
