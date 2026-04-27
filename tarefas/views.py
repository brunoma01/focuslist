from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login

@login_required
def home(request):
    filter_type = request.GET.get('filter', 'all')
    all_tasks = Task.objects.filter(user=request.user).order_by('-id')
    tasks = all_tasks

    if filter_type == 'done':
        tasks = all_tasks.filter(done=True)
    elif filter_type == 'pending':
        tasks = all_tasks.filter(done=False)
    else:
        tasks = all_tasks

    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(done=True).count()
    remaining_tasks = total_tasks - completed_tasks

    pct = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return render(request, 'tarefas/home.html', {
        'tasks': tasks,
        'total': total_tasks,
        'completed': completed_tasks,
        'remaining': remaining_tasks,
        'pct': pct,
        'filter': filter_type,
    })

@require_POST
@login_required
def add(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()

        messages.success(request, 'Tarefa adicionada com sucesso!')
    else:
        messages.error(request, 'Erro ao adicionar tarefa.')

    return redirect('home')

@require_POST
@login_required
def toggle(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.done = not task.done
    task.save()

    if task.done:
        messages.info(request, "Tarefa concluída ✔")
    else:
        messages.info(request, "Tarefa reaberta")

    return redirect('home')

@require_POST
@login_required
def edit(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    
    new_label = request.POST.get('label')

    if new_label:
        task.label = new_label
        task.save()

    return redirect('home')

@require_POST
@login_required
def delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()

    messages.warning(request, "Tarefa removida")

    return redirect('home')

@require_POST
@login_required
def clear_completed(request):
    tasks = Task.objects.filter(user=request.user, done=True)
    total = tasks.count()

    if total > 0:
        tasks.delete()
        messages.warning(request, f"{total} tarefa(s) concluída(s) removida(s)")
    else:
        messages.info(request, "Nenhuma tarefa concluída para limpar")

    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, 'As senhas não coincidem')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, f'Bem-vindo, {username}! Sua conta foi criada com sucesso.')

        return redirect('home')

    return render(request, 'tarefas/register.html')