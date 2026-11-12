from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


@api_view(['POST'])
def register(request):
    # Получаем данные из запроса
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')

    # Валидация: все ли поля заполнены
    if not email or not password or not name:
        return Response(
            {"errors": {"message": "Все поля обязательны"}},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    # Валидация: длина пароля
    if len(password) < 8:
        return Response(
            {"errors": {"password": "Пароль должен быть не менее 8 символов"}},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    # Проверяем, есть ли уже пользователь с таким email
    if User.objects.filter(email=email).exists():
        return Response(
            {"errors": {"email": "Пользователь с таким email уже существует"}},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    # Создаем пользователя (используем email как username)
    user = User.objects.create(
        username=email,
        email=email,
        first_name=name,
        password=make_password(password) # Хешируем пароль для безопасности
    )

    return Response(
        {"success": True, "message": "Пользователь зарегистрирован"},
        status=status.HTTP_201_CREATED
    )





@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Валидация: пустые поля
    if not email or not password:
        return Response(
            {"errors": {"message": "Email и пароль обязательны"}},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    # Пытаемся найти пользователя (так как мы используем email как username)
    user = authenticate(username=email, password=password)

    if user is not None:
        # Для учебного проекта возвращаем заглушку токена (в реальности тут JWT)
        return Response({
            "success": True,
            "token": "test_token_12345",
            "user": {
                "id": user.id,
                "name": user.first_name,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {"errors": {"message": "Неверный email или пароль"}},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


from .models import Course
from .serializers import CourseSerializer
from rest_framework.pagination import PageNumberPagination


# Эндпоинт для получения списка курсов (с пагинацией по 5 штук)
@api_view(['GET'])
def get_courses(request):
    # Получаем все курсы из базы
    courses = Course.objects.all().order_by('-id')  # Сначала новые

    # Настраиваем пагинацию (5 штук на страницу)
    paginator = PageNumberPagination()
    paginator.page_size = 5
    result_page = paginator.paginate_queryset(courses, request)

    # Сериализуем данные (превращаем в JSON)
    serializer = CourseSerializer(result_page, many=True)

    # Возвращаем ответ с данными пагинации
    return paginator.get_paginated_response(serializer.data)

from .models import Enrollment
from django.utils import timezone

# Эндпоинт для записи на курс (покупки)
@api_view(['POST'])
def buy_course(request, course_id):
    # Получаем курс по ID
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"errors": {"message": "Курс не найден"}}, status=status.HTTP_404_NOT_FOUND)

    # Проверяем, авторизован ли пользователь (в реальности тут проверка токена)
    # Для теста будем брать первого пользователя из базы (или того, кто передал email)
    user_email = request.data.get('email')
    if user_email:
        user = User.objects.filter(email=user_email).first()
    else:
        user = User.objects.first() # Заглушка для теста

    if not user:
        return Response({"errors": {"message": "Пользователь не найден"}}, status=status.HTTP_404_NOT_FOUND)

    # Проверяем, не записан ли уже пользователь на этот курс
    if Enrollment.objects.filter(student=user, course=course).exists():
        return Response({"errors": {"message": "Вы уже записаны на этот курс"}}, status=status.HTTP_400_BAD_REQUEST)

    # Создаем запись
    enrollment = Enrollment.objects.create(
        student=user,
        course=course,
        payment_status='pending' # Ожидает оплаты
    )

    # Возвращаем ссылку на оплату (заглушка, как в ТЗ)
    pay_url = f"https://payment.example.com/pay?order_id={enrollment.id}"

    return Response({
        "success": True,
        "pay_url": pay_url,
        "message": "Запись создана, перейдите по ссылке для оплаты"
    }, status=status.HTTP_200_OK)


import random
import string


# Эндпоинт для генерации и проверки сертификата
@api_view(['POST'])
def check_certificate(request):
    # В реальности тут данные приходят с фронтенда, но для теста берем из запроса
    student_id = request.data.get('student_id')
    course_id = request.data.get('course_id')

    if not student_id or not course_id:
        return Response({"errors": {"message": "student_id и course_id обязательны"}},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # 1. ИМИТАЦИЯ ЗАПРОСА К ВНЕШНЕМУ СЕРВЕРУ (service_host)
    # В реальности тут был бы requests.post('http://service_host/create-sertificate', json={...})
    # Но мы сгенерируем 6 случайных цифр для теста
    external_part = str(random.randint(100000, 999999))

    # 2. ГЕНЕРИРУЕМ СВОИ 6 ЦИФР
    internal_part = str(random.randint(100000, 999999))

    # 3. СКЛЕИВАЕМ (12 цифр)
    full_number = external_part + internal_part

    # 4. ПРОВЕРЯЕМ ПОСЛЕДНЮЮ ЦИФРУ (должна быть 1)
    if not full_number.endswith('1'):
        # Если последняя цифра не 1, меняем её на 1
        full_number = full_number[:-1] + '1'

    # 5. СОХРАНЯЕМ В БАЗУ (находим запись и обновляем)
    try:
        enrollment = Enrollment.objects.get(student_id=student_id, course_id=course_id)
        enrollment.certificate_number = full_number
        enrollment.save()

        return Response({
            "success": True,
            "certificate_number": full_number,
            "message": "Сертификат успешно сгенерирован"
        }, status=status.HTTP_200_OK)

    except Enrollment.DoesNotExist:
        return Response({"errors": {"message": "Запись на курс не найдена"}}, status=status.HTTP_404_NOT_FOUND)


# Эндпоинт для Webhook от платежной системы
@api_view(['POST'])
def payment_webhook(request):
    # Получаем ID заказа и статус от платежной системы
    order_id = request.data.get('order_id')
    status_payment = request.data.get('status')  # 'success' или 'failed'

    if not order_id or not status_payment:
        return Response({"errors": {"message": "order_id и status обязательны"}},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    try:
        # Находим запись по ID
        enrollment = Enrollment.objects.get(id=order_id)

        # Обновляем статус (в нашей базе 'paid' или 'failed')
        if status_payment == 'success':
            enrollment.payment_status = 'paid'
        elif status_payment == 'failed':
            enrollment.payment_status = 'failed'
        else:
            return Response({"errors": {"message": "Неверный статус"}}, status=status.HTTP_400_BAD_REQUEST)

        enrollment.save()

        # По ТЗ Webhook должен возвращать код 204 (No Content), без тела ответа
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Enrollment.DoesNotExist:
        return Response({"errors": {"message": "Заказ не найден"}}, status=status.HTTP_404_NOT_FOUND)