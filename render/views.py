from django import forms
from django.db import transaction
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from render.models import Task, Project, ProjectVersion, ProjectTemplate


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ("title", "due_date")


class ProjectCreateForm(ModelForm):
    template = forms.ModelChoiceField(queryset=ProjectTemplate.objects.all(), empty_label="(Nothing)")

    class Meta:
        model = Project
        fields = ("project_name", "template")


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {"disable_create_button": True})


def create_project(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/all-projects')
    return render(request, 'create_project.html', {'form': ProjectCreateForm()})

"""
from django.db.models import OuterRef, Subquery, Max
from myapp.models import Author, Book

latest_book = Book.objects.filter(
    author=OuterRef('pk')
).order_by('-published_date').values('published_date')[:1]

authors_with_latest_book = Author.objects.annotate(
    latest_book_published_date=Subquery(latest_book)
).order_by('name')
"""


def all_projects(request: HttpRequest) -> HttpResponse:
    projects = []
    for project in Project.objects.all():
        project_version = ProjectVersion.objects.filter(project=project).order_by('-pk').first()
        if not project_version:
            project_version = ProjectVersion.objects.create(project=project, version=f"{project.template}-{0}")
        project_version_and_project = {'project_no': project.pk, 'project_version': project_version.version,
                                       'project_name': project.project_name,
                                       'project_version_datetime': project_version.created}
        projects.append(project_version_and_project)

    return render(request, 'all_projects.html', {"projects": projects})


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


@transaction.atomic
def increase_project_version(request: HttpRequest, project_no: int) -> HttpResponse:
    #
    # return list of latest project versions
    increase_project_no(project_no)
    return HttpResponseRedirect('/all-projects')