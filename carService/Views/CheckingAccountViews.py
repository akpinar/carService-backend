import tempfile
import traceback

from django.db.models import Q, Sum
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML

from carService.models import CheckingAccount, PaymentMovement, PaymentType, Profile, ServiceSituation
from carService.models.ApiObject import APIObject
from carService.models.SelectObject import SelectObject
from carService.models.Setting import Setting
from carService.serializers.CheckingAccountSerializer import CheckingAccountPageSerializer, PaymentSerializer, \
    PaymentDiscountSerializer, CheckingAccountPageWithStatisticSerializer
from carService.serializers.GeneralSerializer import SelectSerializer
from carService.services import ButtonServices, DashboardServices
from carService.permissions import IsAccountant, IsAccountantOrAdmin, IsAdmin, IsCustomer, IsCustomerOrAdmin, \
    IsServiceman, IsServicemanOrAdmin


class CheckingAccountApi(APIView):
    permission_classes = (IsAuthenticated, IsCustomerOrAdmin,)

    def get(self, request, format=None):
        checking_accounts = CheckingAccount.objects.all().order_by('-id')
        checking_account_array = []
        for checking_account in checking_accounts:
            data = dict()
            data['checkingAccountId'] = checking_account.uuid
            data['plate'] = checking_account.service.car.plate
            data['serviceDate'] = checking_account.service.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['customerName'] = checking_account.service.car.profile.firmName \
                if checking_account.service.car.profile.isCorporate \
                else checking_account.service.car.profile.user.first_name + ' ' + checking_account.service.car.profile \
                .user.last_name
            data['totalPrice'] = checking_account.service.totalPrice
            data['discount'] = checking_account.service.discount
            data['remainingPrice'] = checking_account.remainingDebt
            data['netPrice'] = checking_account.service.price
            data['taxPrice'] = checking_account.service.totalPrice - checking_account.service.price
            data['paymentSituation'] = checking_account.paymentSituation.name
            data['buttons'] = ButtonServices.get_buttons_payment(checking_account.paymentSituation.name)
            data['serviceNo'] = '#' + str(checking_account.service.pk)
            checking_account_array.append(data)

        api_object = APIObject()
        api_object.data = checking_account_array
        api_object.recordsFiltered = checking_accounts.count()
        api_object.recordsTotal = checking_accounts.count()

        serializer = CheckingAccountPageSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class CheckingAccountStatisticApi(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)

    def get(self, request, format=None):
        total_receivable = CheckingAccount.objects.filter(~Q(paymentSituation__name='Ödendi')).aggregate(
            Sum('remainingDebt'))
        total_price = CheckingAccount.objects.all().aggregate(Sum('service__totalPrice'))

        data = dict()
        data['totalReceivable'] = total_receivable
        data['total_price'] = total_price
        return Response(data, status.HTTP_200_OK)


class CheckingAccountByCustomerApi(APIView):
    permission_classes = (IsAuthenticated, IsCustomerOrAdmin)

    def get(self, request, format=None):
        profile = Profile.objects.get(uuid=request.GET.get('uuid'))
        checking_accounts = CheckingAccount.objects.filter(service__car__profile=profile).order_by('-id')
        checking_account_array = []
        for checking_account in checking_accounts:
            data = dict()
            data['checkingAccountId'] = checking_account.uuid
            data['plate'] = checking_account.service.car.plate
            data['serviceDate'] = checking_account.service.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['customerName'] = checking_account.service.car.profile.firmName \
                if checking_account.service.car.profile.isCorporate \
                else checking_account.service.car.profile.user.first_name + ' ' + checking_account.service.car.profile \
                .user.last_name
            data['totalPrice'] = checking_account.service.totalPrice
            data['discount'] = checking_account.service.discount
            data['remainingPrice'] = checking_account.remainingDebt
            data['netPrice'] = checking_account.service.price
            data['taxPrice'] = checking_account.service.totalPrice - checking_account.service.price
            data['paymentSituation'] = checking_account.paymentSituation.name
            data['buttons'] = ButtonServices.get_buttons_payment(checking_account.paymentSituation.name)
            data['serviceNo'] = '#' + str(checking_account.service.pk)
            checking_account_array.append(data)

        api_object = APIObject()
        api_object.data = checking_account_array
        api_object.recordsFiltered = checking_accounts.count()
        api_object.recordsTotal = checking_accounts.count()
        api_object.remainCheckout = DashboardServices.customer_get_remain(profile.user)
        api_object.totalCheckout = DashboardServices.customer_get_total_checking_account(profile.user)

        serializer = CheckingAccountPageWithStatisticSerializer(api_object, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class PaymentAccountDiscountApi(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)

    def post(self, request, format=None):
        serializer = PaymentDiscountSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "payment is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'paymentAmount':
                    errors_dict['Ödeme Miktarı'] = value
                elif key == 'paymentType':
                    errors_dict['Ödeme Tipi'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class PaymentAccountApi(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)

    def get(self, request, format=None):
        try:
            checking_account = CheckingAccount.objects.get(uuid=request.GET.get('uuid'))
            payment_movements = PaymentMovement.objects.filter(checkingAccount=checking_account).order_by('-id')
            payment_movement_array = []
            for payment_movement in payment_movements:
                data = dict()
                data['paymentAmount'] = payment_movement.paymentAmount
                data['paymentDate'] = payment_movement.creationDate.strftime("%d-%m-%Y %H:%M:%S")
                data['paymentTypeDesc'] = payment_movement.paymentType.name

                payment_movement_array.append(data)

            serializer = PaymentSerializer(payment_movement_array, many=True, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("Başarısız", status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "payment is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'paymentAmount':
                    errors_dict['Ödeme Miktarı'] = value
                elif key == 'paymentType':
                    errors_dict['Ödeme Tipi'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)


class PaymentTypeSelectApi(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)

    def get(self, request, format=None):
        types = PaymentType.objects.filter(~Q(name='İndirim'))
        types_objects = []
        select_object_root = SelectObject()
        select_object_root.label = "Seçiniz"
        select_object_root.value = ""
        types_objects.append(select_object_root)

        for type in types:
            select_object = SelectObject()
            select_object.label = type.name
            select_object.value = type.id
            types_objects.append(select_object)

        serializer = SelectSerializer(types_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)




class GetCheckingAccountPdfApi(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)

    def get(self, request, format=None):
        """Generate pdf."""
        # Model data
        checking_account = CheckingAccount.objects.get(uuid=request.GET.get('uuid'))
        payment_movements = PaymentMovement.objects.filter(checkingAccount=checking_account).order_by('-id')
        payment_movement_array = []
        remain = checking_account.remainingDebt
        for payment_movement in payment_movements:
            data = dict()
            data['paymentAmount'] = payment_movement.paymentAmount
            data['paymentDate'] = payment_movement.creationDate.strftime("%d-%m-%Y %H:%M:%S")
            data['paymentTypeDesc'] = payment_movement.paymentType.name

            payment_movement_array.append(data)

        service = checking_account.service
        car = service.car
        profile = car.profile
        logo = Setting.objects.get(key="logo-dark").value
        total_price = service.totalPrice
        name = ''
        if (profile.firmName):
            name = profile.firmName + "-" + \
                   profile.user.first_name + " " + profile.user.last_name
        else:
            name = profile.user.first_name + " " + profile.user.last_name
        serviceman = service.serviceman.user.first_name + \
                     " " + service.serviceman.user.last_name

        # Rendered
        html_string = render_to_string('pdf.html',
                                       {'paymentMovement': payment_movement_array, 'service': service, 'car': car,
                                        'profile': profile, 'logo': logo, 'name': name,'remain':remain,'totalPrice':total_price})

        html_string=html_string.encode('utf-8').strip()
        html = HTML(string=html_string)
        result = html.write_pdf('tmp/ekstre.pdf')

        # Creating http response
        '''response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=tmp/ekstre.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'r')
            response.write(output.read())'''

        return FileResponse(open('tmp/ekstre.pdf', 'rb'), status=status.HTTP_200_OK,
                            content_type='application/pdf')



