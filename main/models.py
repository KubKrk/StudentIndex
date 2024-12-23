from django.contrib.auth.models import AbstractUser
from django.db import models
import random


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    student_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    GROUP_CHOICES = [
        ('Informatyk', 'Informatyk'),
        ('Zarządzanie', 'Zarządzanie'),
    ]
    group = models.CharField(max_length=15, choices=GROUP_CHOICES, default='Informatyk')

    def save(self, *args, **kwargs):
        if not self.student_number:
            last_user = CustomUser.objects.all().order_by('id').last()
            if last_user and last_user.student_number:
                last_number = int(last_user.student_number[1:])
                self.student_number = f's{last_number + 1:03}'
            else:
                self.student_number = 's001'

        self.username = self.student_number
        super().save(*args, **kwargs)


class Grade(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=2, decimal_places=1, choices=[(x, x) for x in [2.0, 3.0, 3.5, 4.0, 4.5, 5.0]])

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"
