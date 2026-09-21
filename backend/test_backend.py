import unittest
import os
from fastapi.testclient import TestClient

from app import app
from database import init_db, search_products_db, get_product_by_id_db, get_product_by_name_db

class TestBackendAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def test_root_health(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    def test_get_all_products(self):
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertGreaterEqual(len(products), 10)
        self.assertIn("name", products[0])
        self.assertIn("category", products[0])
        self.assertIn("price", products[0])
        self.assertIn("description", products[0])
        self.assertIn("features", products[0])
        self.assertIn("availability", products[0])

    def test_product_search_api(self):
        response = self.client.get("/api/products/search?q=laptop")
        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertGreaterEqual(len(products), 1)
        self.assertTrue(any("laptop" in p["name"].lower() or "laptop" in p["description"].lower() for p in products))

    def test_product_details_api_by_id(self):
        response = self.client.get("/api/products/1")
        self.assertEqual(response.status_code, 200)
        product = response.json()
        self.assertEqual(product["id"], 1)
        self.assertEqual(product["name"], "UltraBook Pro 15")

    def test_product_details_api_by_name(self):
        response = self.client.get("/api/products/details/by-name?name=SonicWave")
        self.assertEqual(response.status_code, 200)
        product = response.json()
        self.assertIn("SonicWave", product["name"])

    def test_product_availability_api_by_id(self):
        response = self.client.get("/api/products/1/availability")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["product_id"], 1)
        self.assertTrue(data["is_in_stock"])
        self.assertGreater(data["stock_quantity"], 0)

    def test_product_availability_api_search(self):
        response = self.client.get("/api/products/availability/search?name=SoundBox")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["is_in_stock"])
        self.assertEqual(data["availability"], "Out of Stock")

    def test_intent_query_integration(self):
        payload = {"intent": "price_query", "query": "smartwatch"}
        response = self.client.post("/api/intent-query", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["intent"], "price_query")
        self.assertIn("FitPulse Smartwatch 4", data["spoken_response"])

if __name__ == "__main__":
    unittest.main()
