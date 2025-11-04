from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# ✅ List all tasks
@login_required
def tasks_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('is_done', 'due_date')
    return render(request, "tasks/list.html", {"tasks": tasks})


# ➕ Add new task
@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect("tasks_list")
    else:
        form = TaskForm()
    return render(request, "tasks/add.html", {"form": form})


# ✏️ Edit task
@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("tasks_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/edit.html", {"form": form})


# 🗑️ Delete task
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    messages.error(request, "Task deleted permanently.")
    return redirect("tasks_list")


# 🔁 Toggle complete status
@login_required
def toggle_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    messages.info(request, f"Task marked as {'done' if task.is_done else 'pending'}.")
    return redirect("tasks_list")
