#!/usr/bin/env python3
"""Static acceptance checks for the Blackjack catalogue routes and media."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODELS = ["6680", "6682", "6683", "6684", "6686", "6687", "6688", "6689", "9914", "9981", "9982", "9983", "6002", "6003", "6533", "6690", "6691"]
SEMANTIC_HERO_MODELS = {"6680": "21", "6682": "33", "6683": "22", "6684": "22", "6686": "33", "6688": "33", "6689": "21", "9914": "21", "9981": "22", "9982": "22", "9983": "33"}
CARBON_MODELS = {"6680", "6682", "6688", "6689", "9914", "9982", "9983"}

class BlackjackCatalogueTests(unittest.TestCase):
    def test_blackjack_index_contract(self):
        page = (ROOT / "blackjack.html").read_text()
        self.assertIn('assets/collections/blackjack.jpg', page)
        for model in MODELS:
            self.assertIn(f"'{model}'", page)
        self.assertIn('blackjack-product.html?model=', page)
        for model in CARBON_MODELS:
            self.assertTrue((ROOT / "assets/photos/blackjack" / model / "21" / f"{model}_21_Carbon.png").is_file())

    def test_blackjack_detail_contract(self):
        page = (ROOT / "blackjack-product.html").read_text()
        for label in ('MODEL', 'SIZE', 'COLLECTION', 'BLACKJACK', 'COLOUR VARIATIONS'):
            self.assertIn(label, page)
        self.assertNotIn('swatch', page.lower())
        self.assertIn('close|openfront|openside', page)
        for model, code in SEMANTIC_HERO_MODELS.items():
            for suffix in ('close.png', 'openfront_main.png', 'openside.png'):
                self.assertTrue((ROOT / 'assets/photos/blackjack' / model / code / f'{model}_{code}{suffix}').is_file())

    def test_blackjack_source_media_is_local_and_not_borrowed(self):
        page = (ROOT / "blackjack-product.html").read_text().lower()
        self.assertNotIn('galaxius', page)
        self.assertNotIn('k-ti', page)
        for path in re.findall(r'assets/photos/blackjack/[\w/.-]+\.png', page):
            self.assertTrue((ROOT / path).is_file(), path)

if __name__ == '__main__':
    unittest.main()
