from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carService.models import Category, Product, ProductCategory
from carService.models.CategoryObject import CategoryObject
from carService.models.CategorySelectObject import CategorySelectObject
from carService.serializers.CategorySerializer import CategorySerializer, CategorySelectSerializer
from carService.serializers.GeneralSerializer import ErrorSerializer
from carService.services import CategoryServices
from carService.permissions import IsAccountant, IsAccountantOrAdmin, IsAdmin, IsCustomer, IsCustomerOrAdmin, \
    IsServiceman, IsServicemanOrAdmin, method_permission_classes


class CategoryApi(APIView):
    permission_classes = (IsAuthenticated,)

    @method_permission_classes((IsServicemanOrAdmin,))
    def get(self, request, format=None):
        if request.GET.get('id') is None:
            categories = Category.objects.filter(isDeleted=False).order_by("-id")
            category_objects = []
            for category in categories:
                category_object = CategoryObject()
                category_object.name = category.name
                category_object.id = category.id
                category_object.parentPath = CategoryServices.get_category_path(category, '')
                category_objects.append(category_object)

            serializer = CategorySerializer(category_objects, many=True, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            category_object = CategoryObject()
            category = Category.objects.get(id=int(request.GET.get('id')))
            category_object.name = category.name
            category_object.id = category.id
            if category.parent:
                category_object.parent = category.parent.id
            else:
                category_object.parent = 0
            # category_object.parentPath = CategoryServices.get_category_path(category, '')
            serializer = CategorySerializer(category_object, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)

    @method_permission_classes((IsServicemanOrAdmin,))
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "category is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'name':
                    errors_dict['Kategori'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsServicemanOrAdmin,))
    def put(self, request, format=None):
        instance = Category.objects.get(id=request.GET.get('id'))
        serializer = CategorySerializer(data=request.data
                                        , instance=instance, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "category is updated"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'name':
                    errors_dict['Kategori'] = value

            return Response(errors_dict, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAdmin,))
    def delete(self, request, format=None):
        category = Category.objects.get(pk=request.GET.get('id'))
        data = dict()
        err = []

        if Category.objects.filter(parent=category).filter(isDeleted=False):

            data['value'] = 'Bu kategori, kaydedilen bir kategoriyle ilişkili olduğu için silinemez'
            err.append(data)
            serializer = ErrorSerializer(err, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_300_MULTIPLE_CHOICES)
        elif ProductCategory.objects.filter(category=category).filter(
                product__in=Product.objects.filter(isDeleted=False)):

            data['value'] = 'Bu kategori, kaydedilen bir ürünle ilişkili olduğu için silinemez'
            err.append(data)
            serializer = ErrorSerializer(err, many=True, context={'request': request})
            print("serialize.data", serializer)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        else:
            category.isDeleted = True
            category.save()
            return Response(status=status.HTTP_200_OK)


class CategorySelectApi(APIView):
    permission_classes = (IsAuthenticated,IsServicemanOrAdmin,)

    def get(self, request, format=None):
        categories = Category.objects.filter(isDeleted=False).order_by("id")
        category_objects = []

        select_object_root = CategorySelectObject()
        select_object_root.label = "Seçiniz"
        select_object_root.value = ""
        category_objects.append(select_object_root)


        category_objectRoot = CategorySelectObject()
        category_objectRoot.label = "Yok"
        category_objectRoot.value = "0"
        category_objects.append(category_objectRoot)
        for category in categories:
            path = CategoryServices.get_category_arr(category, [])
            category_object = CategorySelectObject()
            category_object.value = category.id
            category_object.label = CategoryServices.get_path_from_arr(path)
            category_objects.append(category_object)

        serializer = CategorySelectSerializer(category_objects, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)
