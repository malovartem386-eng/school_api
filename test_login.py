import requests

url = "http://127.0.0.1:8000/api/auth/login"


data = {
    "email": "admin@edu.com",
    "password": "course2025"
}

try:
    response = requests.post(url, json=data)
    print(f"Статус ответа: {response.status_code}")
    print(f"Ответ сервера: {response.json()}")
except Exception as e:
    print(f"Ошибка: {e}")