import os
import tempfile
import unittest

from sticky_notes import load_notes_from_file, save_notes_to_file


class StickyNotesStorageTests(unittest.TestCase):
    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "notes.json")
            notes = [
                {
                    "id": "note-1",
                    "text": "Welcome to Sticky Notes",
                    "x": 120,
                    "y": 80,
                    "width": 240,
                    "height": 220,
                    "color": "#fff59d",
                }
            ]

            save_notes_to_file(path, notes)
            loaded = load_notes_from_file(path)

            self.assertEqual(loaded, notes)

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "missing.json")
            self.assertEqual(load_notes_from_file(path), [])


if __name__ == "__main__":
    unittest.main()
