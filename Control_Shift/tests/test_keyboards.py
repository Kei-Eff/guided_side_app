import unittest
from main import create_app
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["FLASK_ENV"] = "testing"

class TestKeyboards(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    
    def test_keyboard_index(self):
        response = self.client.get("/keyboards/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)


    def test_create_bad_keyboard(self):
        response = self.client.post("/keyboards/", json={"keyboard_name": ""})
        self.assertEqual(response.status_code, 400)

