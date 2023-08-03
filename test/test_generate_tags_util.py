import unittest

import sys

sys.path.append(".")

from src.generate_tags_util import (
    compose_fetch_url,
    AVAILABLE_GENERAL_TAGS_SEARCH_QUERY,
)


class TestGenerateTagsUtil(unittest.TestCase):
    def test_compose_fetch_url(self):
        query = AVAILABLE_GENERAL_TAGS_SEARCH_QUERY
        url = compose_fetch_url(query)

        print(url)

        expected = "https://danbooru.donmai.us/tags.json?page=1&search[hide_empty]=yes&search[order]=count&search[category]=0&search[is_deprecated]=no"

        self.assertEqual(url, expected)


if __name__ == "__main__":
    unittest.main()
