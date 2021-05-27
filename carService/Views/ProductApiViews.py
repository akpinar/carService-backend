from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermissionMetaclass
from rest_framework.views import APIView

from carService.models import Product, Brand, ProductCategory
from carService.models.ApiObject import APIObject
from carService.models.SelectObject import SelectObject
from carService.serializers.GeneralSerializer import SelectSerializer, ErrorSerializer
from carService.serializers.ProductSerializer import ProductSerializer, ProductSerializerr, BrandSerializer, \
    BrandPageSerializer
from rest_framework.response import Response
from carService.permissions import IsAccountant,IsAccountantOrAdmin,IsAdmin,IsCustomer,IsCustomerOrAdmin,IsServiceman,IsServicemanOrAdmin,method_permission_classes

class ProductApi(APIView):
    permission_classes = (IsAuthenticated,)

    @method_permission_classes((IsServicemanOrAdmin,))
    def get(self, request, format=None):
        data = Product.objects.filter(isDeleted=False).order_by('-id')
        serializer = ProductSerializer(data, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    @method_permission_classes((IsServicemanOrAdmin,))
    def post(self, request, format=None):
        serializer = ProductSerializerr(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "product is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'barcodeNumber':
                    errors_dict['Barkod'] = value
                elif key == 'name':
                    errors_dict['Ürün Adı'] = value
                elif key == 'quantity':
                    errors_dict['Stok'] = value
                elif key == 'netPrice':
                    errors_dict['Net Fiyat'] = value
                elif key == 'taxRate':
                    errors_dict['Vergi Oranı'] = value
                elif key == 'categories':
                    errors_dict['Kategori'] = value
                elif key == 'shelf':
                    errors_dict['Raf'] = value
                elif key == 'brand':
                    errors_dict['Marka'] = value
                elif key == 'purchasePrice':
                    errors_dict['Alış Fiyatı'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)
    
    @method_permission_classes((IsServicemanOrAdmin,))
    def put(self, request, format=None):
        instance = Product.objects.get(uuid=request.data['uuid'])
        serializer = ProductSerializerr(data=request.data, instance=instance, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "product is updated"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'barcodeNumber':
                    errors_dict['Barkod'] = value
                elif key == 'name':
                    errors_dict['Ürün Adı'] = value
                elif key == 'quantity':
                    errors_dict['Stok'] = value
                elif key == 'netPrice':
                    errors_dict['Net Fiyat'] = value
                elif key == 'taxRate':
                    errors_dict['Vergi Oranı'] = value
                elif key == 'categories':
                    errors_dict['Kategori'] = value
                elif key == 'shelf':
                    errors_dict['Raf'] = value
                elif key == 'brand':
                    errors_dict['Marka'] = value
                elif key == 'purchasePrice':
                    errors_dict['Alış Fiyatı'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_permission_classes((IsAdmin,))
    def delete(self, request, format=None):
        product = Product.objects.get(uuid=request.GET.get('id'))
        data = dict()
        product.isDeleted = True
        product.save()
        return Response(status=status.HTTP_200_OK)

class SingleProductApi(APIView):
    permission_classes = (IsAuthenticated,IsServicemanOrAdmin,)

    def get(self, request, format=None):
        product = Product.objects.get(uuid=request.GET.get('id'))
        category = ProductCategory.objects.filter(product=product)[0]
        data = dict()
        data['name'] = product.name
        data['brand'] = product.brand.id
        data['taxRate'] = product.taxRate
        data['netPrice'] = product.netPrice
        data['purchasePrice'] = product.purchasePrice
        data['barcodeNumber'] = product.barcodeNumber
        data['quantity'] = product.quantity
        data['shelf'] = product.shelf
        data['productImage'] = product.productImage
        data['categories'] = str(category.category.pk)
        data['isOpen'] = product.isOpen
        data['uuid'] = product.uuid
        serializer = ProductSerializerr(data, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

class SearchProductApi(APIView):
    permission_classes = (IsAuthenticated,IsServicemanOrAdmin,)

    def get(self, request, format=None):
        # data = Product.objects.filter(barcodeNumber__istartswith=request.GET.get('barcode')).order_by('-id')
        data = Product.objects.filter(name__icontains=request.GET.get('barcode')).filter(isDeleted=False).order_by(
            '-id')
        serializer = ProductSerializer(data, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

class BrandApi(APIView):
    permission_classes = (IsAuthenticated,)

    @method_permission_classes((IsServicemanOrAdmin,))
    def get(self, request, format=None):
        if request.GET.get('id') is None:
            data = Brand.objects.filter(isDeleted=False).order_by('-id')
            api_object = APIObject()
            api_object.data = data
            api_object.recordsFiltered = data.count()
            api_object.recordsTotal = data.count()
            serializer = BrandPageSerializer(api_object, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            data = Brand.objects.get(id=int(request.GET.get('id')))
            serializer = BrandSerializer(data, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)

    @method_permission_classes((IsServicemanOrAdmin,))
    def post(self, request, format=None):

        serializer = BrandSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "brand is created"}, status=status.HTTP_200_OK)
        else:

            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'name':
                    errors_dict['Marka'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsServicemanOrAdmin,))
    def put(self, request, format=None):
        instance = Brand.objects.get(id=request.GET.get('id'))
        serializer = BrandSerializer(data=request.data, instance=instance, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "brand is updated"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'name':
                    errors_dict['Marka'] = value
            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)
    
    @method_permission_classes((IsAdmin,))
    def delete(self, request, format=None):
        brand = Brand.objects.get(pk=request.GET.get('id'))
        data = dict()

        if Product.objects.filter(brand=brand):
            data['key'] = '1'
            data['value'] = 'Bu marka, kaydediler bir ürünle ilişkili olduğu için silinemez'
            serializer = ErrorSerializer(data, context={'request': request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            brand.isDeleted = True
            brand.save()
            return Response(status=status.HTTP_200_OK)

class BrandSelectApi(APIView):
    permission_classes = (IsAuthenticated,IsServicemanOrAdmin,)

    def get(self, request, format=None):
        brands = Brand.objects.filter(isDeleted=False)
        brands_objects = []
        select_object_root = SelectObject()
        select_object_root.label = "Seçiniz"
        select_object_root.value = ""
        brands_objects.append(select_object_root)

        for brand in brands:
            select_object = SelectObject()
            select_object.label = brand.name
            select_object.value = brand.id
            brands_objects.append(select_object)

        serializer = SelectSerializer(brands_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
