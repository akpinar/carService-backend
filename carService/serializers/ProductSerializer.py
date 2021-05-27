from rest_framework import serializers

from carService.models import Category, Brand
from carService.models.Product import Product
from carService.models.ProductCategory import ProductCategory
from carService.models.ProductImage import ProductImage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 2


class BrandSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False, required=False)
    name = serializers.CharField(allow_blank=False, allow_null=False, required=True)

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name')
            instance.save()
            return instance

        except Exception:
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            brand = Brand()
            brand.name = validated_data.get('name')
            brand.save()
            return brand
        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")




class BrandPageSerializer(serializers.Serializer):
    data = BrandSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ProductSerializerr(serializers.Serializer):
    barcodeNumber = serializers.CharField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    netPrice = serializers.DecimalField(max_digits=10, decimal_places=2)
    # productImage = serializers.ImageField()
    isOpen = serializers.BooleanField()
    taxRate = serializers.DecimalField(max_digits=10, decimal_places=2)
    # totalProduct = serializers.DecimalField(max_digits=5, decimal_places=2)
    # categories = serializers.ListField(child=serializers.IntegerField())
    categories = serializers.CharField()
    # images = serializers.ListField(child=serializers.CharField())
    productImage = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    shelf = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    brand = serializers.CharField()
    purchasePrice = serializers.DecimalField(max_digits=10, decimal_places=2)
    uuid = serializers.UUIDField(allow_null=True, required=False)

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name')
            instance.barcodeNumber = validated_data.get('barcodeNumber')
            instance.isOpen = validated_data.get('isOpen')
            instance.quantity = validated_data.get('quantity')
            instance.taxRate = validated_data.get('taxRate')
            instance.netPrice = validated_data.get('netPrice')
            instance.shelf = validated_data.get('shelf')
            instance.purchasePrice = validated_data.get('purchasePrice')

            if validated_data.get('productImage') is not None:
                instance.productImage = validated_data.get('productImage')
            instance.totalProduct = validated_data.get('netPrice') + (
                    validated_data.get('netPrice') * validated_data.get('taxRate') / 100)

            instance.brand = Brand.objects.get(pk=int(validated_data.get('brand')))
            instance.save()

            category = Category.objects.get(pk=int(validated_data.get('categories')))
            product_categories = ProductCategory.objects.filter(product=instance)

            for product_category in product_categories:
                product_category.delete()

            product_category = ProductCategory()
            product_category.product = instance
            product_category.category = category
            product_category.save()

            return instance

        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            product = Product()
            product.name = validated_data.get('name')
            product.barcodeNumber = validated_data.get('barcodeNumber')
            product.isOpen = validated_data.get('isOpen')
            product.quantity = validated_data.get('quantity')
            product.taxRate = validated_data.get('taxRate')
            product.netPrice = validated_data.get('netPrice')
            product.shelf = validated_data.get('shelf')
            product.purchasePrice = validated_data.get('purchasePrice')
            product.totalProduct = validated_data.get('netPrice') + (
                    validated_data.get('netPrice') * validated_data.get('taxRate') / 100)

            if validated_data.get('productImage') is not None or validated_data.get('productImage') != '':
                product.productImage = validated_data.get('productImage')
            product.brand = Brand.objects.get(pk=int(validated_data.get('brand')))
            product.save()

            '''productImage = ProductImage()
            productImage.product = product
            productImage.image = validated_data.get('productImage')
            productImage.save()'''

            category = Category.objects.get(pk=int(validated_data.get('categories')))
            productCategory = ProductCategory()
            productCategory.product = product
            productCategory.category = category
            productCategory.save()
            '''for x in validated_data.get('categories'):
                category = Category.objects.get(pk=x)
                productCategory = ProductCategory()
                productCategory.product = product
                productCategory.category = category
                productCategory.save()
'''
            '''for x in validated_data.get('images'):
                productImage = ProductImage()
                productImage.product = product
                productImage.image = x
                productImage.save()'''

            return product

        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")
