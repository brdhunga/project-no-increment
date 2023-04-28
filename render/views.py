from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from render.models import Task, Project, ProjectVersion

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ("title", "due_date")


class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
        fields = ("project_name", "template")


def index(request):
    return render(request, 'index.html', {'form': TaskForm()})


def create_project(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('blah-blah success message')
    return render(request, 'create_project.html', {'form': ProjectCreateForm()})


def all_projects(request: HttpRequest) -> HttpResponse:
    return render(request, 'all_projects.html')


def increase_project_no(project_id: int) -> None:
    project = Project.objects.get(id=project_id)
    project_version = ProjectVersion.objects.filter(project=project).order_by('-pk')
    if project_version.exists():
        version = project_version.first().version
        updated_version_no = int(version.split("-")[-1]) + 1
        ProjectVersion.objects.create(project=project, version=f"{project.template}-{updated_version_no}").save()
    else:
        updated_version_no = 1
        ProjectVersion.objects.create(project=project, version=f"{project.template}-{updated_version_no}").save()


def increase_project_version(request: HttpRequest, project_no: int) -> HttpResponse:
    #
    increase_project_no(project_no)
    return HttpResponse("done..")