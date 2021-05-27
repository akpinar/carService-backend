from rest_framework import serializers


class SelectSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ButtonSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    buttonName = serializers.CharField(read_only=True)
    buttonFunction = serializers.CharField(read_only=True)


class ErrorSerializer(serializers.Serializer):
    value = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
