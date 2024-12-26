from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Group, Subject, Grade
from .forms import CustomUserCreationForm
CustomUser = get_user_model()


class ModelsTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Informatyk")
        self.subject = Subject.objects.create(name="Matematyka", group=self.group)
        self.user = CustomUser.objects.create_user(
            username="s001",
            password="password123",
            student_number="s001",
            group="Informatyk"
        )

    def test_group_str(self):
        self.assertEqual(str(self.group), "Informatyk")

    def test_subject_str(self):
        self.assertEqual(str(self.subject), "Matematyka")

    def test_custom_user_auto_student_number(self):
        user2 = CustomUser.objects.create_user(
            username="s002",  # Ustaw username
            password="password123",
            group="Informatyk"
        )
        self.assertEqual(user2.student_number, "s002")

    def test_grade_str(self):
        grade = Grade.objects.create(student=self.user, subject=self.subject, grade=4.0)
        self.assertEqual(str(grade), "s001 - Matematyka: 4.0")


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.group = Group.objects.create(name="Informatyk")
        self.subject1 = Subject.objects.create(name="Matematyka", group=self.group)
        self.subject2 = Subject.objects.create(name="Fizyka", group=self.group)
        self.user = CustomUser.objects.create_user(
            username="s001",
            password="password123",
            student_number="s001",
            group="Informatyk"
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/register.html')

    def test_dashboard_view(self):
        self.client.login(username="s001", password="password123")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/dashboard.html')

    def test_schedule_view(self):
        self.client.login(username="s001", password="password123")
        response = self.client.get(reverse('schedule'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/schedule.html')
        self.assertContains(response, "Matematyka")

    def test_grades_view_with_empty_grades(self):
        self.client.login(username="s001", password="password123")
        response = self.client.get(reverse('grades'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/grades.html')
        self.assertContains(response, "Matematyka")  # Losowe oceny zostały stworzone

    def test_logout_view(self):
        self.client.login(username="s001", password="password123")
        response = self.client.get(reverse('logout'))  # Użyj GET zamiast POST
        self.assertEqual(response.status_code, 302)  # Powinno przekierować na stronę główną


class FormsTestCase(TestCase):
    def test_custom_user_creation_form_valid(self):
        form_data = {
            'student_number': 's001',  # Musi być jawnie ustawione
            'group': 'Informatyk',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_invalid(self):
        form_data = {
            'student_number': 's001',
            'group': 'Informatyk',
            'password1': 'password123',
            'password2': 'differentpassword'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

