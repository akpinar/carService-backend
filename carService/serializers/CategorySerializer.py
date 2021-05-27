from rest_framework import serializers

from carService.models import Car, Category


class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(allow_null=True, required=False)
    name = serializers.CharField(required=True)
    parent = serializers.CharField(required=True, allow_null=True)
    parentPath = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            category = Category()
            category.name = validated_data.get('name')
            if validated_data.get('parent') != '0':
                parent_category = Category.objects.get(pk=int(validated_data.get('parent')))
                category.parent = parent_category

            category.save()
            return category

        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name')
            if validated_data.get('parent') != 0:
                parent_category = Category.objects.get(pk=int(validated_data.get('parent')))
                instance.parent = parent_category
            instance.save()
            return instance

        except Exception:
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class CategorySelectSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
