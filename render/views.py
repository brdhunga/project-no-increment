from django.forms import forms, ModelForm
from django.shortcuts import render


from render.models import Task

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ("title", "due_date")


def index(request):
    return render(request, 'render/index.html', {'form': TaskForm()})
