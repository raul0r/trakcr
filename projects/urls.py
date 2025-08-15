from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_project, name='create_project'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/create-task/', views.create_task, name='create_task'),
    path('<int:project_id>/create-mvp/', views.create_mvp_requirement, name='create_mvp_requirement'),
    path('task/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('mvp/<int:mvp_id>/toggle/', views.toggle_mvp_requirement, name='toggle_mvp_requirement'),
]
