from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Project, Task, MVPRequirement
from .forms import ProjectForm, TaskForm, MVPRequirementForm


@login_required
def dashboard(request):
    """Dashboard view showing all user's projects"""
    projects = Project.objects.filter(owner=request.user)
    
    # Calculate statistics
    total_projects = projects.count()
    completed_projects = projects.filter(status='completed').count()
    in_progress_projects = projects.filter(status='in_progress').count()
    
    context = {
        'projects': projects,
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'in_progress_projects': in_progress_projects,
    }
    return render(request, 'projects/dashboard.html', context)


@login_required
def project_detail(request, project_id):
    """Detailed view of a specific project"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    tasks = project.task_set.all()
    mvp_requirements = project.mvprequirement_set.all()
    
    context = {
        'project': project,
        'tasks': tasks,
        'mvp_requirements': mvp_requirements,
    }
    return render(request, 'projects/project_detail.html', context)


@login_required
def create_project(request):
    """Create a new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, f'Project "{project.name}" created successfully!')
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    
    return render(request, 'projects/create_project.html', {'form': form})


@login_required
def edit_project(request, project_id):
    """Edit an existing project"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Project "{project.name}" updated successfully!')
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})


@login_required
def create_task(request, project_id):
    """Create a new task for a project"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, f'Task "{task.title}" added successfully!')
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = TaskForm()
    
    return render(request, 'projects/create_task.html', {'form': form, 'project': project})


@login_required
@require_POST
def toggle_task(request, task_id):
    """Toggle task completion status via AJAX"""
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)
    task.toggle_completion()
    
    return JsonResponse({
        'completed': task.completed,
        'completed_date': task.completed_date.strftime('%Y-%m-%d %H:%M') if task.completed_date else None,
        'progress': task.project.get_progress_percentage()
    })


@login_required
@require_POST
def toggle_mvp_requirement(request, mvp_id):
    """Toggle MVP requirement completion status via AJAX"""
    mvp = get_object_or_404(MVPRequirement, id=mvp_id, project__owner=request.user)
    mvp.toggle_completion()
    
    return JsonResponse({
        'completed': mvp.completed,
        'completed_date': mvp.completed_date.strftime('%Y-%m-%d %H:%M') if mvp.completed_date else None,
    })


@login_required
def create_mvp_requirement(request, project_id):
    """Create a new MVP requirement for a project"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    if request.method == 'POST':
        form = MVPRequirementForm(request.POST)
        if form.is_valid():
            mvp = form.save(commit=False)
            mvp.project = project
            mvp.save()
            messages.success(request, 'MVP requirement added successfully!')
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = MVPRequirementForm()
    
    return render(request, 'projects/create_mvp_requirement.html', {'form': form, 'project': project})
