from carService.models.Setting import Setting

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class SettingApi(APIView):
    authentication_classes = []
    def get(self, request, format=None):
        settings = Setting.objects.all()
        data =dict()
        for setting in settings:
            data[setting.key] = setting.value
        return Response(data, status.HTTP_200_OK)