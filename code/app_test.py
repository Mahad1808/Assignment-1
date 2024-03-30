import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Netflix Recommendation System</title>', response.data)

    def test_recommendation_with_title(self):
        response = self.app.get('/recommend?title=SomeMovie')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('movies', data)
        self.assertIn('tv_shows', data)

    def test_recommendation_without_title(self):
        response = self.app.get('/recommend')
        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Please provide a title for recommendation')



if __name__ == '__main__':
    unittest.main()
