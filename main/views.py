from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'main/home.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        last_user = CustomUser.objects.all().order_by('id').last()
        next_student_number = (
            f's{int(last_user.student_number[1:]) + 1:03}' if last_user else 's001'
        )
        form = CustomUserCreationForm(initial={'student_number': next_student_number})
    return render(request, 'main/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html', {'user': request.user})


@login_required
def schedule(request):
    schedule_data = [
        {'day': 'Poniedziałek', 'subject': 'Matematyka', 'time': '10:00-11:30'},
        {'day': 'Wtorek', 'subject': 'Fizyka', 'time': '12:00-13:30'},
    ]
    return render(request, 'main/schedule.html', {'schedule': schedule_data})


@login_required
def grades(request):
    grades_data = [
        {'subject': 'Matematyka', 'grade': '5'},
        {'subject': 'Fizyka', 'grade': '4'},
    ]
    return render(request, 'main/grades.html', {'grades': grades_data})
