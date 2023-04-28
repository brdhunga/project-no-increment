from django.contrib import admin

from render.models import Project, ProjectVersion

# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectVersion)