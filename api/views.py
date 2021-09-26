from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework.parsers import JSONParser

from api.models import Pixochi
from api.serializer import NewPixochiRequestSerializer


@require_POST
def create(request):
    json_data = JSONParser().parse(request)
    serializer = NewPixochiRequestSerializer(data=json_data)
    if serializer.is_valid():
        data = serializer.validated_data
        if Pixochi.objects.filter(pk=data['name']).exists():
            return HttpResponse("This name is occupied", status=400)
        pixochi = Pixochi.objects.create(name=data['name'], eyes=data['eyes'], style=data['filling'])
        return HttpResponse(pixochi.get_state_as_json(), status=200)
    return HttpResponse([serializer.errors[e] for e in serializer.errors], status=400)


@require_GET
def get_state(request, name):
    found = Pixochi.objects.filter(pk=name)
    if not found.exists():
        return HttpResponse("No Pixochi with this name", status=404)
    pixochi = found.get()
    return HttpResponse(pixochi.get_state_as_json())
