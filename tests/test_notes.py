import unittest
from pathlib import Path
import tempfile
import shutil
from src.tools.notes_tools import NotesTools
from src.utils.file_utils import write_markdown_file


class TestNotesTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.notes = NotesTools(self.test_dir)
        
        write_markdown_file(self.test_dir / "note1.md", "# El salto\n\nEste es un libro sobre saltos.")
        write_markdown_file(self.test_dir / "note2.md", "# Python\n\nProgramación en Python.")
        write_markdown_file(self.test_dir / "subfolder" / "note3.md", "# El salto cuántico\n\nFísica cuántica.")
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_search_notes(self):
        results = self.notes.search_notes("El salto")
        self.assertEqual(len(results), 2)
        self.assertTrue(any("note1.md" in r['path'] for r in results))
    
    def test_get_note_content(self):
        result = self.notes.get_note_content("note1.md")
        self.assertIn("El salto", result['content'])
        self.assertIn('metadata', result)
    
    def test_list_recent_notes(self):
        results = self.notes.list_recent_notes(limit=5)
        self.assertLessEqual(len(results), 5)
        self.assertTrue(all('relative_path' in r for r in results))


if __name__ == '__main__':
    unittest.main()
