from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from robots.models import Robot


# Create your views here.
@csrf_exempt
def post(request):
    if request.method == "POST":
        try:
            model = request.headers.get("model")
            version = request.headers.get("version")
            created = request.headers.get("created")
            serial = model + "-" + version
            # Ниже представлена валидация на существующие модели
            # В будущем можно написать код по получения списка из файла или из БД ля сверки
            if model in ["R2", "13", "X5"]:
                result = Robot(
                    serial=serial, model=model, version=version, created=created
                )
                result.save()
            return JsonResponse(
                {
                    "model": model,
                    "version": version,
                    "created": created,
                    "serial": serial,
                }
            )
        except ValueError:
            return JsonResponse(
                {"error": "Check the code", "data": f"{request.headers}"},
            )
    else:
        raise ValueError("It's not a POST request")
