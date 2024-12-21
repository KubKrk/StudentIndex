from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['student_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_number'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.student_number
        if commit:
            user.save()
        return user
