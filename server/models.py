import random
from django.db import models
from django.contrib.auth.models import AbstractUser


grades = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)


def generate_qrcode(length=16, symbols="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return "".join(random.choice(symbols) for _ in range(length))


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.username}'


class Lesson(models.Model):
    teacher = models.ManyToManyField(User, related_name='lessonsUser')
    title = models.CharField(max_length=123)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class Para(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='teachers')
    students = models.ManyToManyField(User, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True)
    end_date = models.DateTimeField(blank=True, null=True)
    qrcode = models.CharField(max_length=16, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.qrcode:
            self.qrcode = generate_qrcode(length=16)
        return super().save(*args, **kwargs)


class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    para = models.ForeignKey(Para, on_delete=models.CASCADE, blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    grade = models.CharField(choices=grades, max_length=10, blank=True)
