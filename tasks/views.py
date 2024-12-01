from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, SubTask
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.urls import reverse

@csrf_exempt
def task_list(request):
    user_id = request.GET.get('user_id')

    if not user_id:
        return JsonResponse({"status": "error", "message": "User ID is missing (task_list)"}, status=400)

    user = User.objects.filter(username=user_id).first()

    if not user:
        return JsonResponse({"status": "error", "message": "User not found (task_list)"}, status=404)

    tasks = Task.objects.prefetch_related('subtasks').filter(user=user)

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'user_id': user_id})

@csrf_exempt
@require_POST
def add_task(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    user_id = request.POST.get('user_id')

    if not user_id:
        return JsonResponse({"status": "error", "message": "User ID is missing (add_task)"}, status=400)

    user = User.objects.filter(username=user_id).first()

    if not user:
        return JsonResponse({"status": "error", "message": "User not found (add_task)"})

    if title:
        Task.objects.create(title=title, description=description, user=user)

    return redirect(reverse('task_list') + f'?user_id={user_id}')

@csrf_exempt
@require_POST
def delete_task(request, task_id):
    user_id = request.POST.get('user_id')
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect(reverse('task_list') + f'?user_id={user_id}')

@csrf_exempt
@require_POST
def toggle_task(request, task_id):
    user_id = request.POST.get('user_id')
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()

    if task.completed and all(subtask.completed for subtask in task.subtasks.all()):
        task.delete()

    return redirect(reverse('task_list') + f'?user_id={user_id}')

@csrf_exempt
@require_POST
def add_subtask(request, task_id):
    user_id = request.POST.get('user_id')
    task = get_object_or_404(Task, id=task_id)
    title = request.POST.get('title')
    if title:
        SubTask.objects.create(title=title, task=task)
    return redirect(reverse('task_list') + f'?user_id={user_id}')

@csrf_exempt
@require_POST
def toggle_subtask(request, subtask_id):
    user_id = request.POST.get('user_id')
    subtask = get_object_or_404(SubTask, id=subtask_id)
    subtask.completed = not subtask.completed
    subtask.save()

    task = subtask.task
    if all(subtask.completed for subtask in task.subtasks.all()) and task.completed:
        task.delete()

    return redirect(reverse('task_list') + f'?user_id={user_id}')

def init_data(request):
    init_data = request.GET.get('initData', None)

    if init_data:
        return JsonResponse({"status": "success", "initData": init_data})
    else:
        return JsonResponse({"status": "error", "message": "initData not found"}, status=400)
