from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Camera, Service
from carService.models.SelectObject import SelectObject
from carService.serializers.GeneralSerializer import SelectSerializer
from carService.permissions import IsAccountant,IsAccountantOrAdmin,IsAdmin,IsCustomer,IsCustomerOrAdmin,IsServiceman,IsServicemanOrAdmin

class CameraSelectApi(APIView):
    permission_classes = (IsAuthenticated,IsAdmin,)

    def get(self, request, format=None):
        cameras = Camera.objects.all()
        cameras_objects = []
        select_object_root = SelectObject()
        select_object_root.label = "Seçiniz"
        select_object_root.value = ""
        cameras_objects.append(select_object_root)

        select_object_no = SelectObject()
        select_object_no.label = "Yok"
        select_object_no.value = 0
        cameras_objects.append(select_object_no)

        for camera in cameras:
            select_object = SelectObject()
            select_object.label = camera.name
            select_object.value = camera.id
            cameras_objects.append(select_object)

        serializer = SelectSerializer(cameras_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

class CameraApiView(APIView):
    permission_classes = (IsAuthenticated,IsCustomerOrAdmin,)

    def get(self, request, format=None):
        service = Service.objects.get(uuid=request.GET.get('uuid'))
        data = dict()
        data['camera'] = service.camera.url
        return Response(data, status.HTTP_200_OK)
