from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    student_number = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.student_number:
            last_user = CustomUser.objects.all().order_by('id').last()
            if last_user:
                last_number = int(last_user.student_number[1:])
                self.student_number = f's{last_number + 1:03}'
            else:
                self.student_number = 's001'
        super().save(*args, **kwargs)
