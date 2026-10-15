
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.views.decorators.http import require_POST

from .models import Task
from .forms import TaskForm


def register(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("task_list")

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )


@login_required
def task_list(request):
    user_tasks = Task.objects.filter(
        user=request.user
    ).order_by("-created_at")

    search_query = request.GET.get("search", "").strip()

    if search_query:
        user_tasks = user_tasks.filter(
            title__icontains=search_query
        )

    status = request.GET.get("status", "")

    if status == "completed":
        user_tasks = user_tasks.filter(completed=True)
    elif status == "pending":
        user_tasks = user_tasks.filter(completed=False)

    stats = Task.objects.filter(user=request.user).aggregate(
        total_count=Count("id"),
        completed_count=Count("id", filter=Q(completed=True)),
        pending_count=Count("id", filter=Q(completed=False)),
    )

    total_count = stats["total_count"]
    completed_count = stats["completed_count"]

    completion_percentage = (
        round((completed_count / total_count) * 100)
        if total_count > 0
        else 0
    )

    paginator = Paginator(user_tasks, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": page_obj,
            "page_obj": page_obj,
            "search_query": search_query,
            "status": status,
            "stats": stats,
            "completion_percentage": completion_percentage,
        },
    )


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            messages.success(request, "Task created successfully!")
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {"form": form},
    )


@login_required
@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user,
    )

    task.completed = not task.completed
    task.save(update_fields=["completed"])

    messages.success(request, "Task status updated!")
    return redirect("task_list")


@login_required
@require_POST
def task_delete(request, pk):
    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user,
    )

    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect("task_list")


@login_required
def task_edit(request, pk):
    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "task": task,
        },
    )
