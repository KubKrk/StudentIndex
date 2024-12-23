from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Subject, Grade, CustomUser
import random


@login_required
def schedule(request):
    """Wyświetla plan zajęć dla zalogowanego studenta"""
    user_group = request.user.group  # Pobierz grupę użytkownika
    subjects = Subject.objects.filter(group__name=user_group)  # Pobierz przedmioty dla grupy użytkownika
    return render(request, 'main/schedule.html', {'schedule': subjects})


@login_required
def grades(request):
    """Wyświetla oceny dla zalogowanego studenta"""
    # Sprawdź, czy użytkownik ma przypisane oceny
    if not Grade.objects.filter(student=request.user).exists():
        # Pobierz przedmioty przypisane do grupy użytkownika
        subjects = Subject.objects.filter(group__name=request.user.group)

        # Utwórz losowe oceny dla użytkownika
        for subject in subjects:
            Grade.objects.create(
                student=request.user,
                subject=subject,
                grade=random.choice([2.0, 3.0, 3.5, 4.0, 4.5, 5.0]),
            )

    # Pobierz przypisane oceny
    grades_data = Grade.objects.filter(student=request.user)
    return render(request, 'main/grades.html', {'grades': grades_data})


def home(request):
    """Strona główna z logowaniem"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'main/home.html', {'form': form})


def register(request):
    """Rejestracja nowego studenta"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        last_user = CustomUser.objects.all().order_by('id').last()
        next_student_number = (
            f's{int(last_user.student_number[1:]) + 1:03}' if last_user and last_user.student_number else 's001'
        )
        form = CustomUserCreationForm(initial={'student_number': next_student_number})
    return render(request, 'main/register.html', {'form': form})


@login_required
def dashboard(request):
    """Główna strona po zalogowaniu"""
    return render(request, 'main/dashboard.html', {'user': request.user})
