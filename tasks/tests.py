
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Task


class TaskManagerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPass123!"
        )

        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

    def test_dashboard_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads(self):
        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Task Manager")

    def test_user_can_create_task(self):
        response = self.client.post(
            reverse("task_create"),
            {
                "title": "Learn Django Testing",
                "description": "Practice automated tests",
            },
        )

        self.assertRedirects(response, reverse("task_list"))

        task = Task.objects.get(title="Learn Django Testing")
        self.assertEqual(task.user, self.user)

    def test_user_sees_only_own_tasks(self):
        Task.objects.create(
            user=self.user,
            title="My Task",
        )

        other_user = User.objects.create_user(
            username="otheruser",
            password="OtherPass123!"
        )

        Task.objects.create(
            user=other_user,
            title="Other User Task",
        )

        response = self.client.get(reverse("task_list"))

        self.assertContains(response, "My Task")
        self.assertNotContains(response, "Other User Task")

    def test_user_cannot_delete_another_users_task(self):
        other_user = User.objects.create_user(
            username="otheruser",
            password="OtherPass123!"
        )

        other_task = Task.objects.create(
            user=other_user,
            title="Protected Task",
        )

        response = self.client.post(
            reverse("task_delete", args=[other_task.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Task.objects.filter(pk=other_task.pk).exists()
        )

    def test_user_can_edit_own_task(self):
        task = Task.objects.create(
            user=self.user,
            title="Old Task",
            description="Old description",
        )

        response = self.client.post(
            reverse("task_edit", args=[task.pk]),
            {
                "title": "Updated Task",
                "description": "Updated description",
            },
        )

        self.assertRedirects(response, reverse("task_list"))

        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Task")
        self.assertEqual(task.description, "Updated description")

    def test_user_can_toggle_own_task(self):
        task = Task.objects.create(
            user=self.user,
            title="Complete Django Tests",
            completed=False,
        )

        response = self.client.post(
            reverse("task_toggle", args=[task.pk])
        )

        self.assertRedirects(response, reverse("task_list"))

        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_user_cannot_edit_another_users_task(self):
        other_user = User.objects.create_user(
            username="otheruser",
            password="OtherPass123!",
        )

        other_task = Task.objects.create(
            user=other_user,
            title="Protected Task",
        )

        response = self.client.post(
            reverse("task_edit", args=[other_task.pk]),
            {
                "title": "Hacked Task",
                "description": "Unauthorized edit",
            },
        )

        self.assertEqual(response.status_code, 404)

        other_task.refresh_from_db()
        self.assertEqual(other_task.title, "Protected Task")

    def test_task_list_pagination(self):
        for i in range(6):
            Task.objects.create(
                user=self.user,
                title=f"Pagination Task {i + 1}",
            )

        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["tasks"]), 5)
        self.assertEqual(
            response.context["page_obj"].paginator.num_pages,
            2,
        )

        response = self.client.get(
            reverse("task_list") + "?page=2"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["tasks"]), 1)

    def test_task_search(self):
        Task.objects.create(
            user=self.user,
            title="Learn Django",
        )
        Task.objects.create(
            user=self.user,
            title="Learn Python",
        )

        response = self.client.get(
            reverse("task_list"),
            {"search": "Django"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Learn Django")
        self.assertNotContains(response, "Learn Python")

    def test_task_status_filter(self):
        Task.objects.create(
            user=self.user,
            title="Completed Task",
            completed=True,
        )
        Task.objects.create(
            user=self.user,
            title="Pending Task",
            completed=False,
        )

        response = self.client.get(
            reverse("task_list"),
            {"status": "completed"},
        )

        self.assertEqual(response.status_code, 200)

        completed_tasks = list(response.context["tasks"])
        completed_titles = [task.title for task in completed_tasks]

        self.assertIn("Completed Task", completed_titles)
        self.assertNotIn("Pending Task", completed_titles)

        response = self.client.get(
            reverse("task_list"),
            {"status": "pending"},
        )

        self.assertEqual(response.status_code, 200)

        pending_tasks = list(response.context["tasks"])
        pending_titles = [task.title for task in pending_tasks]

        self.assertIn("Pending Task", pending_titles)
        self.assertNotIn("Completed Task", pending_titles)
