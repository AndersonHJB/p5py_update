from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CodeShareModel
from django.contrib.auth.models import User


demo_code = '''print("Hello AI悦创")
print("长期招收一对一学员，微信：Jiabcdefh")
'''


def editor(request):
    if request.method == "GET":
        if "id" in request.GET:
            project_id = request.GET["id"]
            project = CodeShareModel.objects.get(project_id=project_id)

            code = project.code.replace("\\", "\\\\")
            code = code.replace("\r\n", "\\n")
            code = code.replace("\n", "\\n")
            code = code.replace("'", "'")
            code = code.replace('"', '"')

            language = project.language
        else:
            code = demo_code.replace('\n', '\\n')
            language = "python"
    return render(
        request, "editor/editor.html", {"code": code, "language": language}
    )


@csrf_exempt
def upload_code(request):
    code = request.POST["code"]
    language = request.POST["language"]
    if request.user.is_authenticated:
        owner = request.user
    else:
        owner = None
    project = CodeShareModel.objects.create(
        code=code, language=language, owner=owner, views=1, likes=1
    )

    project_id = project.project_id
    return JsonResponse({"project_id": project_id})
