import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def print_header(title):
    print("\n" + "="*60)
    print(f" {title} ")
    print("="*60)

# 1. TASK 5 - LOGIN USER
print_header("TASK 5 - LOGIN USER (loginuser)")
login_payload = {"userName": "john_doe", "password": "Password123!"}
res = requests.post(f"{BASE_URL}/api/login/", json=login_payload)
print(f"URL: {res.url}")
print(f"Status: {res.status_code}")
print(f"Response:\n{json.dumps(res.json(), indent=2)}")

# 2. TASK 6 - LOGOUT USER
print_header("TASK 6 - LOGOUT USER (logoutuser)")
res = requests.post(f"{BASE_URL}/api/logout/")
print(f"Status: {res.status_code}")
print(f"Response:\n{json.dumps(res.json(), indent=2)}")

# 3. TASK 8 - DEALER REVIEWS
print_header("TASK 8 - DEALER REVIEWS (getdealerreviews)")
res = requests.get(f"{BASE_URL}/api/dealers/1/reviews/")
print(f"Status: {res.status_code}")
print(f"Response:\n{json.dumps(res.json(), indent=2)}")

# 4. TASK 9 - ALL DEALERS
print_header("TASK 9 - ALL DEALERS (getalldealers)")
res = requests.get(f"{BASE_URL}/api/dealers/")
print(f"Status: {res.status_code}")
print(f"Response:\n{json.dumps(res.json(), indent=2)}")

# 5. TASK 10 - DEALER BY ID
print_header("TASK 10 - DEALER BY ID (getdealerbyid)")
res = requests.get(f"{BASE_URL}/api/dealers/1/")
print(f"Status: {res.status_code}")
print(f"Response:\n{json.dumps(res.json(), indent=2)}")

# 6. TASK 11 - DEALERS BY STATE (KANSAS)
print_header("TASK 11 - DEALERS BY STATE (getdealersbyState)")
res = requests.get(f"{BASE_URL}/api/dealers/?state=Kansas")
print(f"Status: {res.status_code}")
print(f"Response:\n{json.dumps(res.json(), indent=2)}")

# 7. TASKS 14 & 15 - CAR MAKES AND MODELS
print_header("TASKS 14 & 15 - CAR MAKES/MODELS (getallcarmakes)")
res = requests.get(f"{BASE_URL}/api/carmakes/")
print(f"Status: {res.status_code}")
print(f"Response:\n{json.dumps(res.json(), indent=2)}")

# 8. TASK 16 - SENTIMENT ANALYSIS
print_header("TASK 16 - SENTIMENT ANALYSIS (analyzereview)")
sentiment_payload = {"text": "Fantastic services"}
res = requests.post(f"{BASE_URL}/api/analyze-review/", json=sentiment_payload)
print(f"Status: {res.status_code}")
print(f"Response:\n{json.dumps(res.json(), indent=2)}")

# 9. TASK 22 - ADD REVIEW
print_header("TASK 22 - ADD REVIEW (addreview)")
review_payload = {
    "dealer_id": 1,
    "name": "John Doe",
    "review": "Outstanding customer service and smooth car delivery!",
    "rating": 5,
    "purchase": True,
    "purchase_date": "2024-03-01",
    "car_make": "Toyota",
    "car_model": "Camry",
    "car_year": 2023
}
res = requests.post(f"{BASE_URL}/api/reviews/", json=review_payload)
print(f"Status: {res.status_code}")
print(f"Response:\n{json.dumps(res.json(), indent=2)}")
