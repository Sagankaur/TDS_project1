import unittest
import os
import json
from unittest.mock import patch, mock_open, MagicMock

# Import the functions from your script
from tasksB import * #B12, B3, clone_git_repo, B5, B6, B7, B9

class TestPhaseB(unittest.TestCase):
    def setUp(self):
        # Set up temporary test files and directories
        self.test_data_dir = "/data/test"
        self.test_file = os.path.join(self.test_data_dir, "test_file.txt")
        self.test_image = os.path.join(self.test_data_dir, "test_image.jpg")
        self.test_md_file = os.path.join(self.test_data_dir, "test.md")
        self.test_output_file = os.path.join(self.test_data_dir, "output.txt")
        self.test_db = os.path.join(self.test_data_dir, "test.db")
        self.test_url = "http://example.com"
        
        os.makedirs(self.test_data_dir, exist_ok=True)
        with open(self.test_file, "w") as f:
            f.write("Test data")
        with open(self.test_md_file, "w") as f:
            f.write("# Markdown Title\n\nSome content.")

    def tearDown(self):
        # Clean up temporary test files and directories
        if os.path.exists(self.test_data_dir):
            for root, dirs, files in os.walk(self.test_data_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.test_data_dir)

    def test_B12_valid_path(self):
        self.assertTrue(B12("/data/test/file.txt"))

    def test_B12_invalid_path(self):
        self.assertFalse(B12("/invalid/path/file.txt"))

    @patch("requests.get")
    def test_B3_fetch_data_from_api(self, mock_get):
        mock_get.return_value.text = "Mock API response"
        
        save_path = os.path.join(self.test_data_dir, "api_response.txt")
        B3(self.test_url, save_path)
        
        with open(save_path) as f:
            content = f.read()
        
        self.assertEqual(content, "Mock API response")

    @patch("subprocess.run")
    def test_clone_git_repo(self, mock_subprocess_run):
        repo_url = "https://github.com/example/repo.git"
        commit_message = "Test commit"
        
        clone_git_repo(repo_url, commit_message)
        
        mock_subprocess_run.assert_any_call(["git", "clone", repo_url, "/data/repo"])
        mock_subprocess_run.assert_any_call(["git", "-C", "/data/repo", "commit", "-m", commit_message])

    @patch("sqlite3.connect")
    def test_B5_run_sql_query_sqlite(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("row1",), ("row2",)]
        
        query = "SELECT * FROM test_table;"
        result = B5(self.test_db + ".db", query, self.test_output_file)
        
        self.assertEqual(result, [("row1",), ("row2",)])
    
    @patch("requests.get")
    def test_B6_web_scraping(self, mock_get):
        mock_get.return_value.text = "<html><body>Mock HTML</body></html>"
        
        output_file = os.path.join(self.test_data_dir, "scraped.html")
        B6(self.test_url, output_file)
        
        with open(output_file) as f:
            content = f.read()
        
        self.assertEqual(content, "<html><body>Mock HTML</body></html>")

    @patch("PIL.Image.open")
    def test_B7_image_processing_resize(self, mock_open):
        mock_image = MagicMock()
        mock_open.return_value = mock_image
        
        output_file = os.path.join(self.test_data_dir, "resized_image.jpg")
        B7(self.test_image, output_file, resize=(100, 100))
        
        mock_image.resize.assert_called_with((100, 100))
        mock_image.save.assert_called_with(os.path.abspath(output_file))

    @patch("markdown.markdown")
    def test_B9_markdown_to_html_conversion(self, mock_markdown):
        mock_markdown.return_value = "<h1>Markdown Title</h1><p>Some content.</p>"
        
        output_file = os.path.join(self.test_data_dir, "output.html")
        B9(self.test_md_file, output_file)
        
        with open(output_file) as f:
            content = f.read()
        
        self.assertEqual(content, "<h1>Markdown Title</h1><p>Some content.</p>")

if __name__ == "__main__":
    unittest.main()
