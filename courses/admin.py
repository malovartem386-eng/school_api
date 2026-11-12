from django.contrib import admin
from .models import Course, Lesson

# Регистрируем модель Курса в админке
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'hours', 'start_date', 'end_date')
    search_fields = ('title', 'description')

# Регистрируем модель Урока в админке
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration')
    list_filter = ('course',)

from .models import Course, Lesson, Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'payment_status')
    list_filter = ('course', 'payment_status') 
    search_fields = ('student__email', 'student__first_name')