import unittest
import requests

BASE_URL = "http://127.0.0.1:5000"

class TestReceiptsAPI(unittest.TestCase):

    def test_valid_receipt(self):
        receipt = {
            "retailer": "Walmart",
            "total": "20.00",
            "items": [
                {"shortDescription": "Eggs", "price": "5.00"},
                {"shortDescription": "Milk", "price": "4.00"},
                {"shortDescription": "Chocolate", "price": "6.00"}
            ],
            "purchaseDate": "2025-01-25",
            "purchaseTime": "15:30"
        }
        response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
        self.assertEqual(response.status_code, 200)
        receipt_id = response.json().get("id")
        self.assertIsNotNone(receipt_id)

    def test_missing_receipt(self):
        receipt = {}
        response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid receipt data provided.", response.text)

    def test_missing_fields(self):
        receipt = {
            "total": "20.00",
            "items": [],
            "purchaseDate": "2025-01-25",
            "purchaseTime": "15:30"
        }
        response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing receipt field: retailer", response.text)

    def test_points_retrieval(self):
        receipt = {
            "retailer": "Target",
            "total": "10.25",
            "items": [{"shortDescription": "Apples", "price": "5.00"}],
            "purchaseDate": "2025-01-25",
            "purchaseTime": "15:00"
        }
        response = requests.post(f"{BASE_URL}/receipts/process", json=receipt)
        receipt_id = response.json().get("id")

        points_response = requests.get(f"{BASE_URL}/receipts/{receipt_id}/points")
        self.assertEqual(points_response.status_code, 200)
        self.assertEqual(points_response.json().get("points"), 48)

    def test_invalid_receipt_id(self):
        invalid_id = "123e4567-e89b-12d3-a456-426614174000"
        response = requests.get(f"{BASE_URL}/receipts/{invalid_id}/points")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json().get("points"))


if __name__ == "__main__":
    unittest.main()
