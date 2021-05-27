from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Car
from carService.serializers.CarSerializer import CarSerializer
from carService.permissions import IsAccountant, IsAccountantOrAdmin, IsAdmin, IsCustomer, IsCustomerOrAdmin, \
    IsServiceman, IsServicemanOrAdmin, method_permission_classes, IsAll


class CarApi(APIView):
    permission_classes = (IsAuthenticated,)

    @method_permission_classes((IsCustomerOrAdmin,))
    def get(self, request, format=None):
        cars = Car.objects.filter(profile__uuid=request.GET.get('uuid')).filter(isDeleted=False)
        serializer = CarSerializer(cars, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    @method_permission_classes((IsAdmin,))
    def post(self, request, format=None):
        serializer = CarSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "car is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'plate':
                    errors_dict['Plaka'] = value
                elif key == 'brand':
                    errors_dict['Marka'] = value
                elif key == 'model':
                    errors_dict['Model'] = value
                elif key == 'year':
                    errors_dict['Yıl'] = value
                elif key == 'chassisNumber':
                    errors_dict['Şase Numarası'] = value
                elif key == 'currentKM':
                    errors_dict['KM'] = value
                elif key == 'engine':
                    errors_dict['Motor'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAdmin,))
    def put(self, request):
        instance = Car.objects.get(uuid=request.GET.get('id'))
        serializer = CarSerializer(data=request.data, instance=instance, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "car is updated"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'plate':
                    errors_dict['Plaka'] = value
                elif key == 'brand':
                    errors_dict['Marka'] = value
                elif key == 'model':
                    errors_dict['Model'] = value
                elif key == 'year':
                    errors_dict['Yıl'] = value
                elif key == 'chassisNumber':
                    errors_dict['Şase Numarası'] = value
                elif key == 'currentKM':
                    errors_dict['KM'] = value
                elif key == 'engine':
                    errors_dict['Motor'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAdmin,))
    def delete(self, request, format=None):
        car = Car.objects.get(uuid=request.GET.get('id'))
        data = dict()
        car.isDeleted = True
        car.save()

        return Response(status=status.HTTP_200_OK)


class GetCarApi(APIView):


    permission_classes = (IsAuthenticated, IsServicemanOrAdmin | IsCustomer,)
    def get(self, request, format=None):
        cars = Car.objects.get(uuid=request.GET.get('uuid'))
        serializer = CarSerializer(cars, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

