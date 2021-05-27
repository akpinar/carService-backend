from django.conf.urls import url
from django.urls import path

from carService.Views import DashboardViews
from carService.Views.CameraApiViews import CameraSelectApi, CameraApiView
from carService.Views.CarApiViews import CarApi, GetCarApi
from carService.Views.CategoryApiViews import CategoryApi, CategorySelectApi
from carService.Views.CheckingAccountViews import CheckingAccountApi, PaymentAccountApi, PaymentTypeSelectApi, \
    PaymentAccountDiscountApi, CheckingAccountByCustomerApi, GetCheckingAccountPdfApi
from carService.Views.CustomerApiViews import CustomerApi, CustomerGetApi, CustomerSendPasswordApi
from carService.Views.DashboardViews import AdminDashboardViews,ServicemanDashboardViews,CustomerDashboardViews
from carService.Views.ProductApiViews import ProductApi, SearchProductApi, BrandApi, BrandSelectApi, SingleProductApi
from carService.Views.ServiceApiViews import ServiceTypeSelectApi, ServiceApi, GetCarServicesApi, GetServicesApi, \
    GetServiceDetailApi, DeterminationServiceApi, GetServiceProductsApi, GetServiceImagesApi, ServiceCustomerAcceptApi, \
    ServiceProcessingApi,GetServicePdfApi
from carService.Views.StaffViews import StaffApi, ServicemanSelectApi
from carService.Views.UserApiView import UserApi, GroupApi, UserPayload,UserPasswordRegen
from carService.Views.SettingViews import SettingApi

app_name = 'carService'

urlpatterns = [

    url(r'user-api/$', UserApi.as_view(), name='user-api'),
    url(r'password-regen/$', UserPasswordRegen.as_view(), name='password-regen'),
    url(r'user-payload-api/$', UserPayload.as_view()),
    url(r'group-api/$', GroupApi.as_view(), name='group-api'),
    url(r'customer-api/', CustomerApi.as_view(), name='customer-api'),
    url(r'customer-get-api/', CustomerGetApi.as_view(), name='customer-get-api'),
    url(r'customer-send-password-api/', CustomerSendPasswordApi.as_view()),
    url(r'product-api/$', ProductApi.as_view(), name='product-api'),
    url(r'product-single-api/$', SingleProductApi.as_view()),
    url(r'car-api/$', CarApi.as_view(), name='car-api'),
    url(r'category-api/$', CategoryApi.as_view(), name='category-api'),
    url(r'category-select-api/$', CategorySelectApi.as_view(), name='category-select-api'),
    url(r'service-type-select-api/$', ServiceTypeSelectApi.as_view(), name='service-type-select-api'),
    url(r'staff-api/$', StaffApi.as_view(), name='staff-api'),
    url(r'service-api/$', ServiceApi.as_view(), name='service-api'),
    url(r'serviceman-select-api/$', ServicemanSelectApi.as_view(), name='serviceman-select-api'),
    url(r'get-car-by-id-api/$', GetCarApi.as_view(), name='get-car-api'),
    url(r'get-car-services-api/$', GetCarServicesApi.as_view(), name='get-car-services-api'),
    url(r'get-services-api/$', GetServicesApi.as_view(), name='get-services-api'),
    url(r'get-service-detail-api/$', GetServiceDetailApi.as_view(), name='get-services-detail-api'),
    url(r'get-service-pdf-api/$', GetServicePdfApi.as_view(), name='get-services-pdf-api'),
    url(r'get-product-search-api/$', SearchProductApi.as_view()),
    url(r'service-determination-api/$', DeterminationServiceApi.as_view()),
    url(r'get-service-products-api/$', GetServiceProductsApi.as_view()),
    url(r'get-service-images-api/$', GetServiceImagesApi.as_view()),
    url(r'service-approve-api/$', ServiceCustomerAcceptApi.as_view()),
    url(r'brand-api/$', BrandApi.as_view()),
    url(r'brand-select-api/$', BrandSelectApi.as_view()),
    url(r'service-processing-api/$', ServiceProcessingApi.as_view()),
    url(r'checking-account-api/$', CheckingAccountApi.as_view()),
    url(r'payment-account-api/$', PaymentAccountApi.as_view()),
    url(r'payment-type-select-api/$', PaymentTypeSelectApi.as_view()),
    url(r'payment-discount-api/$', PaymentAccountDiscountApi.as_view()),
    url(r'checking-customer-account-api/$', CheckingAccountByCustomerApi.as_view()),
    url(r'camera-select-api/$', CameraSelectApi.as_view()),
    url(r'get-camera-api/$', CameraApiView.as_view()),
    url(r'get-admin-dashboard-api/$', AdminDashboardViews.as_view()),
    url(r'get-serviceman-dashboard-api/$', ServicemanDashboardViews.as_view()),
    url(r'get-customer-dashboard-api/$', CustomerDashboardViews.as_view()),
    url(r'get-settings-api/$', SettingApi.as_view()),
    url(r'get-payment-movement-pdf-api/$', GetCheckingAccountPdfApi.as_view()),



    # url(r'swagger/$', views.schema_view, name='swagger'),

    # url(r'swagger/$', views.schema_view, name='swagger'),

]
