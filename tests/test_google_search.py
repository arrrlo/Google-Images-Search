from google_images_search import search_images

def test_search_images(monkeypatch):
    # Mock response
    class MockResponse:
        def json(self):
            return {
                'items': [
                    {'link': 'https://example.com/image1.jpg'},
                    {'link': 'https://example.com/image2.jpg'}
                ]
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    # Replace requests.get with the mock
    monkeypatch.setattr("requests.get", mock_get)

    results = search_images("cat", "fake_key", "fake_cse_id")

    assert results == [
        'https://example.com/image1.jpg',
        'https://example.com/image2.jpg'
    ]
