"""
Core PDF merging logic — used by backend AND desktop app.
Single source of truth. Never duplicated.
"""
import io
from pathlib import Path
from typing import Union
from pypdf import PdfWriter, PdfReader


def validate_files(file_paths: list[Union[str, Path]]) -> dict:
    """Validate a list of paths before merging."""
    errors = []
    if not file_paths:
        errors.append("No files provided.")
        return {"valid": False, "errors": errors}
    if len(file_paths) < 2:
        errors.append("At least 2 PDF files are required.")
    for path in file_paths:
        p = Path(path)
        if not p.exists():
            errors.append(f"File not found: {p.name}")
        elif p.suffix.lower() != ".pdf":
            errors.append(f"Not a PDF: {p.name}")
        elif p.stat().st_size == 0:
            errors.append(f"File is empty: {p.name}")
    return {"valid": len(errors) == 0, "errors": errors}


def get_pdf_info(file_path: Union[str, Path]) -> dict:
    """Returns page count and filename — used for UI previews."""
    reader = PdfReader(str(file_path))
    return {
        "filename": Path(file_path).name,
        "page_count": len(reader.pages),
        "size_bytes": Path(file_path).stat().st_size,
    }


def merge_pdfs(
    file_paths: list[Union[str, Path]],
    output_path: Union[str, Path, None] = None,
) -> bytes:
    """
    Merge PDFs in order. Returns bytes (for web streaming).
    Optionally writes to disk too (for desktop app).
    """
    writer = PdfWriter()
    for path in file_paths:
        reader = PdfReader(str(path))
        for page in reader.pages:
            writer.add_page(page)

    buffer = io.BytesIO()
    writer.write(buffer)
    pdf_bytes = buffer.getvalue()

    if output_path:
        Path(output_path).write_bytes(pdf_bytes)

    return pdf_bytes