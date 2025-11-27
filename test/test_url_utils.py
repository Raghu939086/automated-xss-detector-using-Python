import unittest
from src.url_utils import parse_url, build_url

class URLUtilsTest(unittest.TestCase):
    def test_parse_and_build(self):
        url = "https://example.com/search?q=hello&id=10"
        base, params = parse_url(url)
        self.assertIn("q", params)
        new = build_url(base, {"q": "PAY", "id": "10"})
        self.assertIn("PAY", new)

if __name__ == "__main__":
    unittest.main()
