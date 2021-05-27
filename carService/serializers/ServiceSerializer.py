import traceback

from rest_framework import serializers

from carService.models import Profile, ServiceSituation, Camera
from carService.models.Car import Car
from carService.models.Service import Service
from carService.models.Situation import Situation
from carService.models.ServiceType import ServiceType
from carService.serializers.GeneralSerializer import ButtonSerializer


class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situation
        fields = '__all__'


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'


class ServiceSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)
    carUUID = serializers.UUIDField()
    serviceType = serializers.CharField()
    # serviceKM = serializers.IntegerField()
    complaint = serializers.CharField()
    serviceSituation = serializers.CharField(read_only=True)
    responsiblePerson = serializers.CharField(allow_null=True, allow_blank=True)
    creationDate = serializers.DateTimeField(read_only=True)
    # serviceman = serializers.CharField(allow_blank=False)
    # actions = serializers.CharField(read_only=True)
    buttons = ButtonSerializer(many=True, read_only=True)
    plate = serializers.CharField(read_only=True)
    # price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    # totalPrice = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    # laborPrice = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    # laborTaxRate = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    # laborName = serializers.CharField(read_only=True)
    # description = serializers.CharField(read_only=True)
    # receiverPerson = serializers.CharField(read_only=True)
    # camera = serializers.CharField(allow_blank=False, required=False, allow_null=True)

    def create(self, validated_data):
        try:
            service = Service()
            service.complaint = validated_data.get('complaint')
            service.car = Car.objects.get(uuid=validated_data.get('carUUID'))
            service.serviceType = ServiceType.objects.get(id=int(validated_data.get('serviceType')))
            service.responsiblePerson = validated_data.get('responsiblePerson')
            # service.serviceKM = int(validated_data.get('serviceKM'))
            # service.serviceman = Profile.objects.get(pk=int(validated_data.get('serviceman')))
            # service.price = 0
            # service.totalPrice = 0
            # service.discount = 0
            # service.laborPrice = 0
            # service.laborTaxRate = 0
            service.save()

            situation = Situation.objects.get(name__exact='Arıza Tespiti Bekleniyor')
            service_situation = ServiceSituation()
            service_situation.service = service
            service_situation.situation = situation

            service_situation.save()
            return service

        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        pass


class ServicePageSerializer(serializers.Serializer):
    data = ServiceSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
    activePage = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ServiceImageSerializer(serializers.Serializer):
    image = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
