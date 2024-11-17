# test_integration.py
import requests
import json
import time

BASE_URL = "http://localhost:8000"  # Kong API Gateway URL
AUTH_URL = "http://localhost:8081"

class EcommerceTest:
    def __init__(self):
        self.token = None
        self.products = []
        self.orders = []

    def authenticate(self):
        """Get authentication token"""
        response = requests.post(
            f"{AUTH_URL}/auth/login",
            json={"username": "user", "password": "pass"}
        )
        self.token = response.json()["token"]
        print(f"Authentication successful. Token: {self.token[:20]}...")

    def get_headers(self):
        """Get headers with authentication"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_products(self):
        """Create test products"""
        products = [
            {
                "name": "Gaming Laptop",
                "price": 1299.99,
                "description": "High-end gaming laptop",
                "stock": 50
            },
            {
                "name": "Smartphone Pro",
                "price": 899.99,
                "description": "Latest smartphone model",
                "stock": 100
            }
        ]

        for product in products:
            response = requests.post(
                f"{BASE_URL}/products",
                headers=self.get_headers(),
                json=product
            )
            if response.status_code == 200:
                self.products.append(response.json())
                print(f"Created product: {product['name']}")
            else:
                print(f"Failed to create product: {response.text}")

    def create_order(self):
        """Create a test order"""
        if not self.products:
            print("No products available to order")
            return

        order = {
            "userId": "user123",
            "items": [
                {
                    "productId": self.products[0]["id"],
                    "quantity": 1,
                    "price": self.products[0]["price"]
                }
            ],
            "totalAmount": self.products[0]["price"],
            "status": "PENDING"
        }

        response = requests.post(
            f"{BASE_URL}/orders",
            headers=self.get_headers(),
            json=order
        )
        
        if response.status_code == 200:
            self.orders.append(response.json())
            print(f"Created order: {response.json()}")
        else:
            print(f"Failed to create order: {response.text}")

    def verify_data(self):
        """Verify created data through GET endpoints"""
        # Verify products
        response = requests.get(
            f"{BASE_URL}/products",
            headers=self.get_headers()
        )
        print("\nAll Products:")
        print(json.dumps(response.json(), indent=2))

        # Verify orders
        if self.orders:
            order_id = self.orders[0]["id"]
            response = requests.get(
                f"{BASE_URL}/orders/{order_id}",
                headers=self.get_headers()
            )
            print("\nOrder Details:")
            print(json.dumps(response.json(), indent=2))

def run_tests():
    test = EcommerceTest()
    
    print("Starting integration tests...")
    test.authenticate()
    time.sleep(1)
    
    test.create_products()
    time.sleep(1)
    
    test.create_order()
    time.sleep(1)
    
    test.verify_data()

if __name__ == "__main__":
    run_tests()