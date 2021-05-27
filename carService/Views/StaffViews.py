from django.contrib.auth.models import Group, User
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Profile
from carService.models.ApiObject import APIObject
from carService.models.SelectObject import SelectObject
from carService.serializers.GeneralSerializer import SelectSerializer
from carService.serializers.UserSerializer import StaffSerializer, StaffPageSerializer, StaffSingleSerializer
from carService.permissions import IsAccountant, IsAccountantOrAdmin, IsAdmin, IsCustomer, IsCustomerOrAdmin, \
    IsServiceman, IsServicemanOrAdmin, method_permission_classes


class StaffApi(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)

    def get(self, request, format=None):
        '''  search = request.GET.get('search')

          per_page = request.GET.get('per_page')
          page = request.GET.get('page')
          page = int(page) - 1
          start = (int(page) * int(per_page))
          end = start + int(per_page)

          data = Profile.objects.filter(user__groups__name__iexact='Repairman').filter(
              Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) |
              Q(firmName__icontains=search)).order_by('-id')[start:end]
  '''
        if request.GET.get('id') is None:
            # data = Profile.objects.filter(~Q(user__groups__name__iexact=request.Get.get('name')))
            data = Profile.objects.filter(~Q(user__groups__name__iexact='Customer')).filter(isDeleted=False)
            apiObject = APIObject()
            apiObject.data = data
            apiObject.recordsFiltered = data.count()
            apiObject.recordsTotal = data.count()
            serializer = StaffPageSerializer(apiObject, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)

        else:
            profile = Profile.objects.get(uuid=request.GET.get('id'))
            data = dict()
            data['firstName'] = profile.user.first_name
            data['lastName'] = profile.user.last_name
            data['username'] = profile.user.username
            data['mobilePhone'] = profile.mobilePhone
            data['address'] = profile.address
            data['group'] =profile.user.groups.filter()[0].id
            data['uuid'] = profile.uuid
            serializer = StaffSingleSerializer(data, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):

        serializer = StaffSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "repairman is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'group':
                    errors_dict['Grup'] = value
                elif key == 'username':
                    errors_dict['Email'] = value
                elif key == 'firstName':
                    errors_dict['İsim'] = value
                elif key == 'lastName':
                    errors_dict['Soyisim'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAdmin,))
    def delete(self, request, format=None):
        try:

            profile = Profile.objects.get(uuid=request.GET.get('id'))
            profile.isDeleted = True
            profile.user.is_active = False
            profile.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_permission_classes((IsServicemanOrAdmin,))
    def put(self, request, format=None):
        instance = Profile.objects.get(uuid=request.GET.get('id'))
        serializer = StaffSerializer(data=request.data, instance=instance, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Staff is updated"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'group':
                    errors_dict['Grup'] = value
                elif key == 'username':
                    errors_dict['Email'] = value
                elif key == 'firstName':
                    errors_dict['İsim'] = value
                elif key == 'lastName':
                    errors_dict['Soyisim'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class ServicemanSelectApi(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)

    def get(self, request, format=None):
        servicemans = Profile.objects.filter(user__groups__name__exact='Tamirci').filter(isDeleted=False)
        serviceman_objects = []
        select_object_root = SelectObject()
        select_object_root.label = "Seçiniz"
        select_object_root.value = ""
        serviceman_objects.append(select_object_root)

        for serviceman in servicemans:
            select_object = SelectObject()
            select_object.label = serviceman.user.first_name + ' ' + serviceman.user.last_name
            select_object.value = serviceman.id
            serviceman_objects.append(select_object)

        serializer = SelectSerializer(serviceman_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
