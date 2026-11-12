from rest_framework import serializers
from .models import Course, Lesson

# Сериализатор для Курса
class CourseSerializer(serializers.ModelSerializer):
    # Переопределяем названия полей, чтобы они совпадали с ТЗ (name вместо title)
    name = serializers.CharField(source='title')
    img = serializers.ImageField(source='image', required=False)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'hours', 'img', 'start_date', 'end_date', 'price']