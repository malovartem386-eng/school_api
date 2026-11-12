import requests
url = "http://127.0.0.1:8000/api/payment/webhook"

data = {
    "order_id": 3,
    "status": "success"
}

response = requests.post(url, json=data)

print(f"Статус ответа: {response.status_code}")
