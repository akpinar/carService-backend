import traceback

from rest_framework import serializers

from carService.models import Supplier


class SupplierSerializer(serializers.Serializer):
    firmName = serializers.CharField(required=True)
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    firstName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lastName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    creationDate = serializers.DateTimeField(read_only=True)
    modificationDate = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            supplier = Supplier()
            supplier.firmName = validated_data.get('firmName')
            supplier.address = validated_data.get('address')
            supplier.phone = validated_data.get('phone')
            supplier.firstName = validated_data.get('firstName')
            supplier.lastName = validated_data.get('lastName')
            supplier.save()

            return supplier
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
