import unittest

from google_images_search.google_api import GoogleCustomSearch


class TestGoogleApi(unittest.TestCase):

    def setUp(self):
        self._api_key = '__api_key__'
        self._api_cx = '__api_cx__'
        self._api = GoogleCustomSearch(self._api_key, self._api_cx)

    def test_init(self):
        self.assertEqual(self._api._developer_key, self._api_key)
        self.assertEqual(self._api._custom_search_cx, self._api_cx)
        self.assertEqual(self._api._google_build, None)
        self.assertEqual(self._api._search_params_keys, {
            'q': None,
            'searchType': 'image',
            'num': 1,
            'imgType': None,
            'imgSize': None,
            'fileType': None,
            'safe': 'off',
            'imgDominantColor': None
        })

    def test_search_params(self):
        params = {
            'q': 'test',
        }
        assert_params = {
            'q': 'test',
            'num': 1,
            'safe': 'off',
            'searchType': 'image'
        }
        self.assertEqual(self._api._search_params(params), assert_params)

        params = {
            'q': 'test',
            'num': 12,
            'imgDominantColor': 'black'
        }
        assert_params = {
            'q': 'test',
            'num': 12,
            'safe': 'off',
            'searchType': 'image',
            'imgDominantColor': 'black'
        }
        self.assertEqual(self._api._search_params(params), assert_params)

        params = {
            'q': 'test',
            'num': 1,
            'safe': 'high',
            'fileType': 'jpg',
            'imgType': 'clipart',
            'imgSize': 'huge',
            'searchType': 'image',
            'imgDominantColor': 'black'
        }
        self.assertEqual(self._api._search_params(params), params)
