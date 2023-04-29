from django.contrib import admin

from render.models import Project, ProjectVersion, ProjectTemplate

# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectVersion)
admin.site.register(ProjectTemplate)