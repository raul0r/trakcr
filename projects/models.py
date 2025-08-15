from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):
    """Model representing a creator's project"""
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    progress = models.IntegerField(default=0, help_text="Progress percentage (0-100)")
    due_date = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_date']
        
    def __str__(self):
        return self.name
    
    def get_progress_percentage(self):
        """Calculate progress based on completed tasks"""
        total_tasks = self.task_set.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.task_set.filter(completed=True).count()
        return int((completed_tasks / total_tasks) * 100)
    
    def get_next_task(self):
        """Get the next incomplete task"""
        return self.task_set.filter(completed=False).first()
    
    def get_last_completed_task(self):
        """Get the most recently completed task"""
        return self.task_set.filter(completed=True).order_by('-completed_date').first()


class Task(models.Model):
    """Model representing a task within a project"""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    completed_date = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'created_date']
        
    def __str__(self):
        return f"{self.project.name} - {self.title}"
    
    def toggle_completion(self):
        """Toggle task completion status"""
        self.completed = not self.completed
        if self.completed:
            self.completed_date = timezone.now()
        else:
            self.completed_date = None
        self.save()


class MVPRequirement(models.Model):
    """Model representing MVP requirements for a project"""
    
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    completed_date = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'created_date']
        
    def __str__(self):
        return f"{self.project.name} MVP - {self.description[:50]}..."
    
    def toggle_completion(self):
        """Toggle MVP requirement completion status"""
        self.completed = not self.completed
        if self.completed:
            self.completed_date = timezone.now()
        else:
            self.completed_date = None
        self.save()
