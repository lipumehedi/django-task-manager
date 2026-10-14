
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def task_list(request):
    tasks = Task.objects.all().order_by("-created_at")

    search_query = request.GET.get("search", "")
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    status = request.GET.get("status", "")
    if status == "completed":
        tasks = tasks.filter(completed=True)
    elif status == "pending":
        tasks = tasks.filter(completed=False)

    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": tasks,
            "search_query": search_query,
            "status": status,
        },
    )


def task_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            Task.objects.create(
                title=title,
                description=description,
            )

        return redirect("task_list")

    return render(request, "tasks/task_form.html")


def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.completed = not task.completed
        task.save()

    return redirect("task_list")


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()

    return redirect("task_list")


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            task.title = title
            task.description = description
            task.save()
            return redirect("task_list")

    return render(
        request,
        "tasks/task_form.html",
        {"task": task},
    )
