import unittest
from pathlib import Path
import tempfile
import shutil
from src.tools.logseq_tools import LogseqTools
from src.utils.file_utils import read_markdown_file


class TestLogseqTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.logseq = LogseqTools(self.test_dir)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_create_page(self):
        result = self.logseq.create_page("Test Page", "# Content\n\nTest content")
        self.assertTrue(Path(result['path']).exists())
        
        content = read_markdown_file(Path(result['path']))
        self.assertIn("Test content", content)
    
    def test_create_page_no_overwrite(self):
        self.logseq.create_page("Test Page", "First content")
        result = self.logseq.create_page("Test Page", "Second content", overwrite=False)
        
        content = read_markdown_file(Path(result['path']))
        self.assertIn("First content", content)
        self.assertIn("Second content", content)
    
    def test_update_page_append(self):
        self.logseq.create_page("Test Page", "Original content")
        result = self.logseq.update_page("Test Page", "New content", append=True)
        
        content = read_markdown_file(Path(result['path']))
        self.assertIn("Original content", content)
        self.assertIn("New content", content)
    
    def test_create_journal_entry(self):
        result = self.logseq.create_journal_entry("Journal content", date="2024_01_15")
        self.assertTrue(Path(result['path']).exists())
        
        content = read_markdown_file(Path(result['path']))
        self.assertIn("Journal content", content)
    
    def test_sanitize_filename(self):
        safe_name = self.logseq._sanitize_filename("Test: Page/Name?")
        self.assertNotIn(":", safe_name)
        self.assertNotIn("/", safe_name)
        self.assertNotIn("?", safe_name)


if __name__ == '__main__':
    unittest.main()
