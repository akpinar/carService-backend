import json

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.serializers.DashboardSerializer import AdminDashboardSerializer, ServicemanDashboardSerializer, \
    CustomerDashboardSerializer
from carService.services import DashboardServices
from carService.permissions import IsAccountant, IsAccountantOrAdmin, IsAdmin, IsCustomer, IsCustomerOrAdmin, \
    IsServiceman, IsServicemanOrAdmin


class AdminDashboardViews(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)

    def get(self, request, format=None):
        data = dict()
        data['productCount'] = DashboardServices.get_product_count()
        data['outOfStockCount'] = DashboardServices.get_product_out_of_stock_count()
        data['carCount'] = DashboardServices.get_car_count()
        data['customerCount'] = DashboardServices.get_customer_count()
        data['remainingDebt'] = DashboardServices.get_remain()
        data['uncompletedServiceCount'] = DashboardServices.get_uncompleted_services_count()
        data['waitingApproveServiceCount'] = DashboardServices.get_waiting_approve_services_count()
        data['completedServiceCount'] = DashboardServices.get_completed_services_count()
        data['totalCheckingAccountDaily'] = DashboardServices.get_total_checking_account('daily')
        data['totalCheckingAccountMonthly'] = DashboardServices.get_total_checking_account('monthly')
        data['totalCheckingAccountYearly'] = DashboardServices.get_total_checking_account('yearly')
        data['canceledServiceCount'] = DashboardServices.get_canceled_services_count()
        data['lineChartIncome'] =DashboardServices.get_total_checking_account_for_line_chart()
        serializer = AdminDashboardSerializer(data, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class ServicemanDashboardViews(APIView):
    permission_classes = (IsAuthenticated, IsServiceman,)

    def get(self, request, format=None):
        data = dict()
        data['uncompletedServiceCount'] = DashboardServices.serviceman_get_uncompleted_services_count(request.user)
        data[
            'waitingCustomerApproveServiceCount'] = DashboardServices.serviceman_get_waiting_customer_approve_services_count(
            request.user)
        data['waitingApproveServiceCount'] = DashboardServices.serviceman_get_waiting_approve_services_count(
            request.user)
        data['completedServiceCount'] = DashboardServices.serviceman_get_completed_services_count(request.user)
        data['canceledServiceCount'] = DashboardServices.serviceman_get_canceled_services_count(request.user)
        serializer = ServicemanDashboardSerializer(data, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class CustomerDashboardViews(APIView):
    permission_classes = (IsAuthenticated, IsCustomer,)

    def get(self, request, format=None):
        data = dict()
        data['carCount'] = DashboardServices.customer_get_car_count(request.user)
        data['uncompletedServiceCount'] = DashboardServices.customer_get_uncompleted_services_count(request.user)
        data['waitingApproveServiceCount'] = DashboardServices.customer_get_waiting_approve_services_count(request.user)
        data['completedServiceCount'] = DashboardServices.customer_get_completed_services_count(request.user)
        data['canceledServiceCount'] = DashboardServices.customer_get_canceled_services_count(request.user)
        data['remainingDebt'] = DashboardServices.customer_get_remain(request.user)
        data['totalCheckingAccount'] = DashboardServices.customer_get_total_checking_account(request.user)
        serializer = CustomerDashboardSerializer(data, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
