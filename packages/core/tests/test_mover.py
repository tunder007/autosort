from pathlib import Path

from core.pipeline import sort_folder


def test_sort_folder_moves_files(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4")
    (tmp_path / "b.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 8)

    result = sort_folder(tmp_path, dry_run=False)

    assert result.files_moved == 2
    assert (tmp_path / "pdf_folder" / "a.pdf").is_file()
    assert (tmp_path / "png_folder" / "b.png").is_file()
    assert not (tmp_path / "a.pdf").exists()


def test_dry_run_does_not_move(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4")
    result = sort_folder(tmp_path, dry_run=True)
    assert result.files_moved == 1
    assert (tmp_path / "a.pdf").is_file()
