from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task, Bid
from .forms import TaskForm, BidForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('task_list')

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    bids = task.bids.all().order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.task = task
            bid.freelancer = request.user
            bid.save()
            return redirect('task_detail', pk=task.pk)
    else:
        bid_form = BidForm()

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'bids': bids,
        'bid_form': bid_form
    })

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    task = bid.task
    
    if request.user == task.created_by:
        task.status = 'Assigned'
        task.save()
        
    return redirect('task_detail', pk=task.id)
