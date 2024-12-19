import datetime
from datetime import datetime, timedelta

import pandas as pd
from django.http import HttpResponse, JsonResponse

from robots.models import Robot

# Create your views here.


def download_excel(request) -> HttpResponse:
    # нужно отфильтровать за последнюю неделю
    now = datetime.now()
    one_week_ago = now - timedelta(weeks=1)
    robots_data = Robot.objects.filter(created__gte=one_week_ago)

    data = {}

    for object in robots_data:
        if object.model not in data:
            data[object.model] = {
                "Модель": [],
                "Версия": [],
                "Количество за неделю": [],
            }

            data[object.model]["Модель"].append(object.model)
            data[object.model]["Версия"].append(object.version)
            data[object.model]["Количество за неделю"].append(1)
        elif (
            object.model in data[object.model]["Модель"]
            and object.version not in data[object.model]["Версия"]
        ):
            data[object.model]["Модель"].append(object.model)
            data[object.model]["Версия"].append(object.version)
            data[object.model]["Количество за неделю"].append(1)
        else:
            index_of_version = data[object.model]["Версия"].index(object.version)
            data[object.model]["Количество за неделю"][index_of_version] += 1

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="summary.xlsx"'

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        for name in data.keys():
            # DataFrame
            df = pd.DataFrame(data[name])
            df.to_excel(writer, index=False, sheet_name=f"{name}")

    return response
