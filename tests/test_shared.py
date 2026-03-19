import io
import pytest
from pathlib import Path
from pypdf import PdfWriter
from mergepdf_shared import merge_pdfs, validate_files, get_pdf_info


def make_pdf(tmp_path: Path, name: str, pages: int = 1) -> Path:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=612, height=792)
    path = tmp_path / name
    with open(path, "wb") as f:
        writer.write(f)
    return path


class TestValidateFiles:
    def test_empty_is_invalid(self):
        assert validate_files([])["valid"] is False

    def test_single_file_invalid(self, tmp_path):
        pdf = make_pdf(tmp_path, "one.pdf")
        assert validate_files([pdf])["valid"] is False

    def test_two_pdfs_valid(self, tmp_path):
        a, b = make_pdf(tmp_path, "a.pdf"), make_pdf(tmp_path, "b.pdf")
        assert validate_files([a, b])["valid"] is True

    def test_non_pdf_flagged(self, tmp_path):
        txt = tmp_path / "doc.txt"
        txt.write_text("hello")
        pdf = make_pdf(tmp_path, "real.pdf")
        result = validate_files([txt, pdf])
        assert result["valid"] is False
        assert any("doc.txt" in e for e in result["errors"])


class TestMergePdfs:
    def test_returns_valid_pdf_bytes(self, tmp_path):
        a, b = make_pdf(tmp_path, "a.pdf", 2), make_pdf(tmp_path, "b.pdf", 3)
        result = merge_pdfs([a, b])
        assert isinstance(result, bytes)
        assert result[:4] == b"%PDF"

    def test_correct_page_count(self, tmp_path):
        a, b = make_pdf(tmp_path, "a.pdf", 2), make_pdf(tmp_path, "b.pdf", 3)
        reader = __import__("pypdf").PdfReader(io.BytesIO(merge_pdfs([a, b])))
        assert len(reader.pages) == 5

    def test_saves_to_disk(self, tmp_path):
        a, b = make_pdf(tmp_path, "a.pdf"), make_pdf(tmp_path, "b.pdf")
        out = tmp_path / "merged.pdf"
        merge_pdfs([a, b], output_path=out)
        assert out.exists() and out.stat().st_size > 0