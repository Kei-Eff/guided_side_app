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
        self.assertIn(b'<h1>Keyboard Index</h1>', response.data)


    def test_create_bad_keyboard(self):
        response = self.client.post("/keyboards/", data={"keyboard_name": ""})
        self.assertEqual(response.status_code, 400)

    def test_create_good_keyboard(self):
        response = self.client.post("/keyboards/", data={"keyboard_name": "testkeyboard"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["keyboard_name"], "testkeyboard")
        self.client.delete(f"/keyboards/{response.get_json()['keyboard_id']}/")
    
    def test_delete_keyboard(self):
        response1 = self.client.post("/keyboards/", data={"keyboard_name": "testkeyboard"})
        id = response1.get_json()["keyboard_id"]
        
        response2 = self.client.delete(f"keyboards/{id}/")
        self.assertEqual(response2.status_code, 200)

    def test_update_keyboard(self):
        response1 = self.client.post("/keyboards/", data={"keyboard_name": "testkeyboard"})
        id = response1.get_json()["keyboard_id"]

        response2 = self.client.put(f"/keyboards/{id}", data={"keyboard_name": "newtestkeyboard"})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.get_json()["keyboard_name"], "newtestkeyboard")

        self.client.delete(f"/keyboards/{id}/")