from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=250)
    due_date = models.DateField(default=timezone.now)


class Project(models.Model):
    project_name = models.CharField(max_length=250) #, help_text="Enter a name for the project")
    template = models.CharField(max_length=250, choices=[('A', 'A'), ('B', 'B')])

    def __str__(self):
        return self.project_name


class ProjectVersion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=100, default="", null=True)

    def __str__(self):
        return f"Project version {self.version} for {self.project}"
