from rest_framework import serializers

from carService.models import Profile, Car
from carService.serializers.UserSerializer import CustomerAddSerializer


class CarSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False)
    plate = serializers.CharField(required=True)
    brand = serializers.CharField(required=True)
    model = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)
    engine = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    profileUuid = serializers.UUIDField(required=False,  allow_null=True)
    oilType = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    chassisNumber = serializers.CharField(required=True)
    currentKM = serializers.CharField(required=True)
    engineNumber = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    color = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    profile = CustomerAddSerializer(read_only=True)

    def create(self, validated_data):
        try:
            profile = Profile.objects.get(uuid=validated_data.get('profileUuid'))
            car = Car()
            if profile:
                car.brand = validated_data.get('brand')
                car.color = validated_data.get('color')
                car.currentKM = validated_data.get('currentKM')
                car.chassisNumber = validated_data.get('chassisNumber')
                car.profile = profile
                car.model = validated_data.get('model')
                car.year = validated_data.get('year')
                car.engine = validated_data.get('engine')
                car.oilType = validated_data.get('oilType')
                car.engineNumber = validated_data.get('engineNumber')
                car.plate = validated_data.get('plate')
                car.save()

            return car
        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:
            instance.brand = validated_data.get('brand')
            instance.color = validated_data.get('color')
            instance.currentKM = validated_data.get('currentKM')
            instance.chassisNumber = validated_data.get('chassisNumber')
            instance.model = validated_data.get('model')
            instance.year = validated_data.get('year')
            instance.engine = validated_data.get('engine')
            instance.oilType = validated_data.get('oilType')
            instance.engineNumber = validated_data.get('engineNumber')
            instance.plate = validated_data.get('plate')
            instance.save()
            return instance

        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")
