import json
import os
import tkinter as tk
from tkinter import colorchooser, messagebox
from typing import List, Dict, Any


DATA_FILE = os.path.join(os.path.expanduser("~"), ".sticky_notes.json")


def save_notes_to_file(path: str, notes: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(notes, handle, indent=2)


def load_notes_from_file(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


class StickyNote(tk.Toplevel):
    def __init__(self, master, note_data: Dict[str, Any], on_delete):
        super().__init__(master)
        self.on_delete = on_delete
        self.note_data = note_data
        self.title("Sticky Note")
        self.overrideredirect(True)
        self.configure(bg="#fff59d")
        self.geometry(f"{note_data['width']}x{note_data['height']}+{note_data['x']}+{note_data['y']}")
        self.resizable(False, False)

        self.text_widget = tk.Text(self, wrap="word", bg="#fff59d", fg="#333", bd=0, padx=10, pady=10)
        self.text_widget.insert("1.0", note_data.get("text", ""))
        self.text_widget.pack(fill="both", expand=True)

        self.bind("<B1-Motion>", self._move_note)
        self.bind("<Button-3>", self._show_context_menu)
        self.text_widget.bind("<B1-Motion>", self._move_note)
        self.text_widget.bind("<Button-3>", self._show_context_menu)

        self._build_context_menu()

    def _build_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Change color", command=self._change_color)
        self.context_menu.add_command(label="Delete", command=self._delete_note)

    def _move_note(self, event):
        self.geometry(f"+{event.x_root - 100}+{event.y_root - 50}")
        self.note_data["x"] = self.winfo_x()
        self.note_data["y"] = self.winfo_y()

    def _show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def _change_color(self):
        color = colorchooser.askcolor(title="Choose note color", color=self.note_data.get("color", "#fff59d"))[1]
        if color:
            self.note_data["color"] = color
            self.configure(bg=color)
            self.text_widget.configure(bg=color)

    def _delete_note(self):
        self.on_delete(self)
        self.destroy()


class StickyNotesApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sticky Notes")
        self.root.geometry("280x120")
        self.root.configure(bg="#f7f7f7")
        self.notes = []
        self.note_windows = []
        self.data_file = DATA_FILE

        self._create_ui()
        self._load_notes()

    def _create_ui(self):
        self.root.bind("<Control-n>", self._create_note)
        self.root.bind("<Control-s>", self._save_notes)

        frame = tk.Frame(self.root, bg="#f7f7f7")
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        tk.Label(frame, text="Sticky Notes", font=("Segoe UI", 16, "bold"), bg="#f7f7f7").pack(anchor="w")
        tk.Label(frame, text="Ctrl+N: new note   Ctrl+S: save", bg="#f7f7f7").pack(anchor="w", pady=(4, 12))

        tk.Button(frame, text="New Note", command=self._create_note).pack(fill="x", pady=(0, 6))
        tk.Button(frame, text="Save Notes", command=self._save_notes).pack(fill="x")

    def _create_note(self, event=None):
        note = {
            "id": f"note-{len(self.notes) + 1}",
            "text": "New note",
            "x": 50 + len(self.notes) * 30,
            "y": 50 + len(self.notes) * 30,
            "width": 240,
            "height": 220,
            "color": "#fff59d",
        }
        self.notes.append(note)
        window = StickyNote(self.root, note, self._remove_note)
        self.note_windows.append(window)
        self._save_notes()

    def _remove_note(self, note_window):
        self.notes = [note for note in self.notes if note.get("id") != note_window.note_data.get("id")]
        self.note_windows = [n for n in self.note_windows if n is not note_window]
        self._save_notes()

    def _save_notes(self, event=None):
        save_notes_to_file(self.data_file, self.notes)

    def _load_notes(self):
        notes = load_notes_from_file(self.data_file)
        self.notes = notes
        for note in notes:
            StickyNote(self.root, note, self._remove_note)


def main():
    root = tk.Tk()
    StickyNotesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
