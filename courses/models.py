from django.db import models
from PIL import Image


# Модель для Курса
class Course(models.Model):
    # Название (макс 30 символов, обязательно)
    title = models.CharField(max_length=30)

    # Описание (макс 100 символов, обязательно)
    description = models.CharField(max_length=100)

    # Продолжительность в часах (целое число, не больше 10)
    hours = models.IntegerField()

    # Цена (в формате xxx.xx, не меньше 100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Даты начала и окончания
    start_date = models.DateField()
    end_date = models.DateField()

    # Обложка (картинка)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Вызываем стандартное сохранение
        super().save(*args, **kwargs)

        # Если есть картинка, обрабатываем её
        if self.image:
            img = Image.open(self.image.path)

            # Если размер больше 300x300, сжимаем
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)  # Сохраняет пропорции, вписывая в 300x300
                img.save(self.image.path)  # Перезаписываем файл


# Модель для Урока
class Lesson(models.Model):
    # Привязка к курсу
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    # Заголовок (макс 50 символов)
    title = models.CharField(max_length=50)

    # Текстовое содержание (необязательно)
    content = models.TextField(blank=True)

    # Видеоссылка
    video_link = models.URLField(blank=True)

    # Длительность в часах (целое, не более 4)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# Модель для записи студента на курс (Заказ)
class Enrollment(models.Model):
    # Связь со студентом (используем стандартную модель User)
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='enrollments')

    certificate_number = models.CharField(max_length=20, null=True, blank=True)

    # Связь с курсом
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')

    # Дата записи (автоматически ставится текущая дата)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    # Статус оплаты (ожидает, оплачено, ошибка)
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('failed', 'Ошибка оплаты'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"