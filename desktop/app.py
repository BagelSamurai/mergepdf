"""
MergePDF Desktop App
Built with CustomTkinter — modern styled UI on top of Tkinter.
Uses mergepdf_shared for all PDF logic (same as the web backend).
"""

import threading
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox

from mergepdf_shared import merge_pdfs, validate_files, get_pdf_info

# ── Appearance ──────────────────────────────────────────────────────────────
ctk.set_appearance_mode("system")       # follows OS light/dark mode
ctk.set_default_color_theme("blue")


# ── File row widget ──────────────────────────────────────────────────────────

class FileRow(ctk.CTkFrame):
    """
    A single row in the file list.
    Shows filename, page count, and up/down/remove buttons.
    """

    def __init__(self, parent, pdf_file: dict, on_move, on_remove, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.pdf_file = pdf_file
        self.on_move = on_move
        self.on_remove = on_remove
        self._build()

    def _build(self):
        self.grid_columnconfigure(1, weight=1)

        # Index label (set externally via update_index)
        self.index_label = ctk.CTkLabel(
            self, text="1", width=24,
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
        )
        self.index_label.grid(row=0, column=0, padx=(4, 8))

        # File info
        info_frame = ctk.CTkFrame(self, fg_color=("gray95", "gray20"), corner_radius=8)
        info_frame.grid(row=0, column=1, sticky="ew", pady=3)
        info_frame.grid_columnconfigure(0, weight=1)

        name = self.pdf_file["filename"]
        pages = self.pdf_file.get("page_count")
        size_kb = self.pdf_file["size_bytes"] / 1024

        size_str = (
            f"{size_kb / 1024:.1f} MB" if size_kb > 1024 else f"{size_kb:.0f} KB"
        )
        detail = f"{size_str} · {pages} pages" if pages else f"{size_str} · loading..."

        ctk.CTkLabel(
            info_frame, text=name,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, padx=12, pady=(6, 0), sticky="w")

        ctk.CTkLabel(
            info_frame, text=detail,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w",
        ).grid(row=1, column=0, padx=12, pady=(0, 6), sticky="w")

        # Move buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=4)

        ctk.CTkButton(
            btn_frame, text="▲", width=28, height=22,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            border_width=1,
            command=lambda: self.on_move(self.pdf_file["id"], "up"),
        ).pack(pady=(0, 2))

        ctk.CTkButton(
            btn_frame, text="▼", width=28, height=22,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            border_width=1,
            command=lambda: self.on_move(self.pdf_file["id"], "down"),
        ).pack()

        # Remove button
        ctk.CTkButton(
            self, text="✕", width=28, height=28,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color=("gray50", "gray60"),
            hover_color=("gray85", "gray30"),
            command=lambda: self.on_remove(self.pdf_file["id"]),
        ).grid(row=0, column=3, padx=(4, 2))

    def update_index(self, index: int):
        self.index_label.configure(text=str(index))


# ── Main window ──────────────────────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MergePDF")
        self.geometry("560x640")
        self.minsize(480, 500)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # State: list of dicts with id, filename, path, page_count, size_bytes
        self._files: list[dict] = []
        self._row_widgets: dict[str, FileRow] = {}
        self._id_counter = 0

        self._build_header()
        self._build_dropzone()
        self._build_file_list()
        self._build_footer()

    # ── Build UI sections ────────────────────────────────────────────────────

    def _build_header(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 0))

        ctk.CTkLabel(
            frame, text="MergePDF",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(side="left")

        # Appearance toggle
        self._mode_btn = ctk.CTkButton(
            frame, text="☀ Light", width=80, height=28,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=1,
            command=self._toggle_mode,
        )
        self._mode_btn.pack(side="right")

    def _build_dropzone(self):
        self._drop_frame = ctk.CTkFrame(
            self, corner_radius=12,
            border_width=2,
            border_color=("gray70", "gray40"),
        )
        self._drop_frame.grid(row=1, column=0, sticky="ew", padx=24, pady=16)
        self._drop_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self._drop_frame,
            text="Drop PDFs here",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, pady=(20, 4))

        ctk.CTkLabel(
            self._drop_frame,
            text="or",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
        ).grid(row=1, column=0)

        ctk.CTkButton(
            self._drop_frame,
            text="Browse files",
            width=130, height=34,
            font=ctk.CTkFont(size=13),
            command=self._browse_files,
        ).grid(row=2, column=0, pady=(8, 20))

    def _build_file_list(self):
        # Scrollable container for file rows
        self._list_frame = ctk.CTkScrollableFrame(
            self, label_text="",
            fg_color=("gray97", "gray15"),
            corner_radius=12,
        )
        self._list_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=0)
        self._list_frame.grid_columnconfigure(0, weight=1)

        # Placeholder shown when list is empty
        self._placeholder = ctk.CTkLabel(
            self._list_frame,
            text="No files added yet",
            font=ctk.CTkFont(size=13),
            text_color=("gray60", "gray50"),
        )
        self._placeholder.grid(row=0, column=0, pady=40)

    def _build_footer(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=3, column=0, sticky="ew", padx=24, pady=16)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)

        self._clear_btn = ctk.CTkButton(
            frame, text="Clear all",
            height=38, font=ctk.CTkFont(size=13),
            fg_color="transparent",
            border_width=1,
            state="disabled",
            command=self._clear_all,
        )
        self._clear_btn.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self._merge_btn = ctk.CTkButton(
            frame, text="Merge PDFs",
            height=38, font=ctk.CTkFont(size=13, weight="bold"),
            state="disabled",
            command=self._start_merge,
        )
        self._merge_btn.grid(row=0, column=1, sticky="ew")

        # Status label below buttons
        self._status_label = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
        )
        self._status_label.grid(row=4, column=0, pady=(0, 12))

    # ── File management ──────────────────────────────────────────────────────

    def _browse_files(self):
        paths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")],
        )
        if paths:
            self._add_files(list(paths))

    def _add_files(self, paths: list[str]):
        for path in paths:
            self._id_counter += 1
            file_id = str(self._id_counter)
            p = Path(path)

            entry = {
                "id": file_id,
                "path": path,
                "filename": p.name,
                "size_bytes": p.stat().st_size,
                "page_count": None,
            }
            self._files.append(entry)

            # Fetch page count in a background thread (keeps UI responsive)
            threading.Thread(
                target=self._load_info,
                args=(file_id, path),
                daemon=True,
            ).start()

        self._refresh_list()

    def _load_info(self, file_id: str, path: str):
        """Runs in a background thread — fetches page count, then updates UI."""
        try:
            info = get_pdf_info(path)
            for f in self._files:
                if f["id"] == file_id:
                    f["page_count"] = info["page_count"]
                    break
            # Schedule UI update back on the main thread
            self.after(0, self._refresh_list)
        except Exception:
            pass

    def _remove_file(self, file_id: str):
        self._files = [f for f in self._files if f["id"] != file_id]
        self._refresh_list()

    def _move_file(self, file_id: str, direction: str):
        idx = next((i for i, f in enumerate(self._files) if f["id"] == file_id), -1)
        if idx == -1:
            return
        new_idx = idx - 1 if direction == "up" else idx + 1
        if 0 <= new_idx < len(self._files):
            self._files[idx], self._files[new_idx] = (
                self._files[new_idx], self._files[idx],
            )
        self._refresh_list()

    def _clear_all(self):
        self._files.clear()
        self._refresh_list()

    # ── UI refresh ───────────────────────────────────────────────────────────

    def _refresh_list(self):
        """Rebuild the file list UI from current state."""

        # Destroy all existing rows
        for widget in self._row_widgets.values():
            widget.destroy()
        self._row_widgets.clear()

        has_files = len(self._files) > 0

        if has_files:
            self._placeholder.grid_remove()
            for i, f in enumerate(self._files):
                row = FileRow(
                    self._list_frame, f,
                    on_move=self._move_file,
                    on_remove=self._remove_file,
                )
                row.grid(row=i, column=0, sticky="ew", padx=8, pady=2)
                row.update_index(i + 1)
                self._row_widgets[f["id"]] = row
        else:
            self._placeholder.grid()

        # Update button states
        can_merge = len(self._files) >= 2
        self._merge_btn.configure(
            state="normal" if can_merge else "disabled",
            text=f"Merge {len(self._files)} PDFs" if can_merge else "Merge PDFs",
        )
        self._clear_btn.configure(state="normal" if has_files else "disabled")

        total_pages = sum(f["page_count"] or 0 for f in self._files)
        if has_files:
            self._status_label.configure(
                text=f"{len(self._files)} files · {total_pages} pages total"
            )
        else:
            self._status_label.configure(text="")

    # ── Merge ────────────────────────────────────────────────────────────────

    def _start_merge(self):
        """Validate, pick output path, then merge in a background thread."""
        paths = [f["path"] for f in self._files]

        result = validate_files(paths)
        if not result["valid"]:
            messagebox.showerror("Invalid files", "\n".join(result["errors"]))
            return

        output_path = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF file", "*.pdf")],
            initialfile="merged.pdf",
        )
        if not output_path:
            return  # user cancelled

        # Disable UI while merging
        self._merge_btn.configure(state="disabled", text="Merging…")
        self._clear_btn.configure(state="disabled")
        self._status_label.configure(text="Merging...")

        threading.Thread(
            target=self._do_merge,
            args=(paths, output_path),
            daemon=True,
        ).start()

    def _do_merge(self, paths: list[str], output_path: str):
        """Runs in background thread — does the actual merge."""
        try:
            merge_pdfs(paths, output_path=output_path)
            self.after(0, self._on_merge_success, output_path)
        except Exception as e:
            self.after(0, self._on_merge_error, str(e))

    def _on_merge_success(self, output_path: str):
        self._status_label.configure(text=f"Saved to {Path(output_path).name}")
        self._refresh_list()
        messagebox.showinfo(
            "Done!",
            f"PDFs merged successfully.\n\nSaved to:\n{output_path}"
        )

    def _on_merge_error(self, error: str):
        self._refresh_list()
        messagebox.showerror("Merge failed", f"Something went wrong:\n{error}")

    # ── Theme toggle ─────────────────────────────────────────────────────────

    def _toggle_mode(self):
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self._mode_btn.configure(
            text="☀ Light" if new_mode == "Dark" else "☾ Dark"
        )


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()