from ninja import NinjaAPI

from render.models import Project, ProjectVersion
from render.views import increase_project_no

api = NinjaAPI()


@api.get("/get-version")
def get_latest_project_version(request, project_no: int):
    """"""
    project_version = ProjectVersion.objects.filter(project_id=project_no)\
        .order_by('-pk').first()
    return {"version": project_version.version}


@api.get("/update-version")
def update_project_version(request, project_no: int):
    """"""
    increase_project_no(project_no)
    project_version = ProjectVersion.objects.filter(project_id=project_no)\
        .order_by('-pk').first()
    return {"version": project_version.version}
