from pathlib import Path

from core.folders import create_type_folders, folder_name_for_type
from core.scanner import scan_folder


def test_create_type_folders(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4")
    (tmp_path / "b.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 8)
    matrix = scan_folder(tmp_path)

    created = create_type_folders(tmp_path, matrix)
    assert (tmp_path / folder_name_for_type("pdf")).is_dir()
    assert (tmp_path / folder_name_for_type("png")).is_dir()
    assert len(created) == 2
