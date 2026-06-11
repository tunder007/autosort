from pathlib import Path

from core.detector import detect_type


def test_detect_pdf_by_magic(tmp_path: Path) -> None:
    file = tmp_path / "doc.pdf"
    file.write_bytes(b"%PDF-1.4 test")
    assert detect_type(file) == "pdf"


def test_detect_png_by_extension(tmp_path: Path) -> None:
    file = tmp_path / "photo.png"
    file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 8)
    assert detect_type(file) == "png"


def test_unknown_extension(tmp_path: Path) -> None:
    file = tmp_path / "data.xyz"
    file.write_text("hello")
    assert detect_type(file) == "unknown"
