from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework.parsers import JSONParser

from api.exception import NameOccupiedError, PixochiNotFoundError, PixochiDeadError
from api.models import Pixochi
from api.serializer import NewPixochiRequestSerializer


@require_POST
def create(request):
    json_data = JSONParser().parse(request)
    serializer = NewPixochiRequestSerializer(data=json_data)
    if serializer.is_valid():
        data = serializer.validated_data
        try:
            pixochi = Pixochi.create(data['name'], data['eyes'], data['filling'])
            return HttpResponse(pixochi.get_state_as_json(), status=200)
        except NameOccupiedError as e:
            return HttpResponse(e.message, status=400)
    return HttpResponse([serializer.errors[e] for e in serializer.errors], status=400)


@require_GET
def get_state(request, name):
    try:
        pixochi = Pixochi.get(name)
        return HttpResponse(pixochi.get_state_as_json())
    except PixochiNotFoundError as e:
        return HttpResponse(e.message, status=404)


@require_POST
def nurse(request):
    name = request.body.decode()
    try:
        pixochi = Pixochi.get(name)
        pixochi.nurse()
        return HttpResponse(pixochi.get_state_as_json())
    except PixochiNotFoundError as e:
        return HttpResponse(e.message, status=404)
    except PixochiDeadError as e:
        return HttpResponse(e.message, status=400)
