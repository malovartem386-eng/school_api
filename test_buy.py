import requests

# ID курса, который хотим купить (admin)
course_id = 4
url = f"http://127.0.0.1:8000/api/courses/{course_id}/buy"

# Данные для запроса (передаем email пользователя, чтобы сервер знал, кто покупает)
data = {
    "email": "admin@edu.com"
}

try:
    response = requests.post(url, json=data)
    print(f"Статус ответа: {response.status_code}")
    print(f"Ответ сервера: {response.json()}")
except Exception as e:
    print(f"Ошибка: {e}")