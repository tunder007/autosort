from pathlib import Path

from core.scanner import scan_folder


def test_scan_top_level_only(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4")
    (tmp_path / "b.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 8)
    sub = tmp_path / "nested"
    sub.mkdir()
    (sub / "c.txt").write_text("ignored")

    matrix = scan_folder(tmp_path)
    assert len(matrix) == 2
    assert matrix[0].type == "pdf"
    assert matrix[1].type == "png"
    assert len(matrix[0].paths) == 1
    assert matrix[0].paths[0].name == "a.pdf"
