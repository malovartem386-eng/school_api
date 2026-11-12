from django.urls import path
from . import views

urlpatterns = [
    path('auth/register', views.register, name='register'),
    path('auth/login', views.login, name='login'),
    path('courses', views.get_courses, name='get_courses'),
    path('courses/<int:course_id>/buy', views.buy_course, name='buy_course'),
    path('certificate/check', views.check_certificate, name='check_certificate'),
    path('payment/webhook', views.payment_webhook, name='payment_webhook'),
]