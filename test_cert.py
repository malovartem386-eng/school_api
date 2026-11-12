import requests

url = "http://127.0.0.1:8000/api/certificate/check"

# ID пользователя (admin@edu.com) и ID курса (админ)
data = {
    "student_id": 3,  # ID пользователя
    "course_id": 4   # ID курса
}

response = requests.post(url, json=data)

print(f"Статус ответа: {response.status_code}")
print(f"Ответ сервера: {response.json()}")