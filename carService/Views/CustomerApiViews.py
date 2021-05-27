from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Profile, Car, Service
from carService.models.ApiObject import APIObject
from carService.serializers.GeneralSerializer import ErrorSerializer
from carService.serializers.UserSerializer import CustomerAddSerializer, CustomerPageSerializer, CustomerGetSerializer
from carService.permissions import IsAccountant, IsAccountantOrAdmin, IsAdmin, IsCustomer, IsCustomerOrAdmin, \
    IsServiceman, IsServicemanOrAdmin, method_permission_classes
from carService.services import MailServices


class CustomerApi(APIView):
    permission_classes = (IsAuthenticated,)

    @method_permission_classes((IsAccountantOrAdmin | IsCustomer,))
    def get(self, request, format=None):

        search = request.GET.get('search')
        """
        per_page = request.GET.get('per_page')
        page = request.GET.get('page')
        page = int(page) - 1
        start = (int(page) * int(per_page))
        end = start + int(per_page)
        """
        user = User.objects.get(id=request.user.id)
        group_name = request.user.groups.filter()[0].name

        data = None
        if group_name == 'Customer':
            data = Profile.objects.filter(user=user).filter(user__groups__name__iexact='Customer').filter(
                isDeleted=False).filter(
                Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) |
                Q(firmName__icontains=search)).order_by('-id')
        else:
            data = Profile.objects.filter(user__groups__name__iexact='Customer').filter(isDeleted=False).filter(
                Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) |
                Q(firmName__icontains=search)).order_by('-id')

        apiObject = APIObject()
        apiObject.data = data
        apiObject.recordsFiltered = data.count()
        apiObject.recordsTotal = Profile.objects.filter(user__groups__name__iexact='Customer').count()

        serializer = CustomerPageSerializer(apiObject, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    @method_permission_classes((IsAdmin,))
    def post(self, request, format=None):
        serializer = CustomerAddSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user is created"}, status=status.HTTP_200_OK)
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
                elif key == 'firmName':
                    errors_dict['Firma Adı'] = value
                elif key == 'taxNumber':
                    errors_dict['Vergi Numarası'] = value
                elif key == 'taxOffice':
                    errors_dict['Vergi Dairesi'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAdmin,))
    def delete(self, request, format=None):
        profile = Profile.objects.get(uuid=request.GET.get('id'))
        user = profile.user
        data = dict()
        err = []
        try:
            if Car.objects.filter(isDeleted=False, profile=profile):
                data['value'] = 'Bu Müşterinin, sistemde aracı yada araçları kayıtlı olduğu için silinemez'
                err.append(data)
                serializer = ErrorSerializer(err, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_300_MULTIPLE_CHOICES)

            elif Service.objects.filter(car__in=Car.objects.filter(profile=profile)):
                data['value'] = 'Bu Müşterinin, sistemde servis kaydı yada kayıtları olduğu için silinemez'
                err.append(data)
                serializer = ErrorSerializer(err, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_300_MULTIPLE_CHOICES)

            else:
                profile.isDeleted = True
                profile.save()
                user.is_active = False
                user.save()
                return Response(status=status.HTTP_200_OK)
        except:
            data['value'] = 'Beklenmeyen hata.'
            err.append(data)
            serializer = ErrorSerializer(err, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_permission_classes((IsServicemanOrAdmin,))
    def put(self, request, format=None):
        instance = Profile.objects.get(uuid=request.GET.get('id'))
        serializer = CustomerAddSerializer(data=request.data, instance=instance, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer is updated"}, status=status.HTTP_200_OK)
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
                elif key == 'firmName':
                    errors_dict['Firma Adı'] = value
                elif key == 'taxNumber':
                    errors_dict['Vergi Numarası'] = value
                elif key == 'taxOffice':
                    errors_dict['Vergi Dairesi'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class CustomerGetApi(APIView):
    permission_classes = (IsAuthenticated,)

    @method_permission_classes((IsAccountantOrAdmin | IsCustomer,))
    def get(self, request, format=None):
        profile = Profile.objects.get(uuid=request.GET.get('id'))
        data = dict()
        data['firstName'] = profile.user.first_name
        data['lastName'] = profile.user.last_name
        data['username'] = profile.user.username
        data['mobilePhone'] = profile.mobilePhone
        data['address'] = profile.address
        data['firmName'] = profile.firmName
        data['taxOffice'] = profile.taxOffice
        data['taxNumber'] = profile.taxNumber
        data['isCorporate'] = profile.taxNumber
        data['uuid'] = profile.uuid
        serializer = CustomerGetSerializer(data, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class CustomerSendPasswordApi(APIView):
    permission_classes = (IsAuthenticated,)

    @method_permission_classes((IsAccountantOrAdmin | IsCustomer,))
    def post(self, request, format=None):
        profile = Profile.objects.get(uuid=request.GET.get('id'))
        if request.GET.get('type') == 'sendMail':
            if profile.isSendMail:
                profile.isSendMail = False
            else:
                profile.isSendMail = True

            profile.save()

        else:
            user = profile.user
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            MailServices.send_password(password=password, to=user.email)

        return Response(None, status.HTTP_200_OK)
