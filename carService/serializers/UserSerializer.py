import traceback

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from carService.services import MailServices
from carService.models.Profile import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'is_active', 'groups']
        depth = 2


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserAddSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    gender = serializers.CharField(required=False)
    firstName = serializers.CharField(required=False)
    lastName = serializers.CharField(required=False)
    username = serializers.CharField(write_only=True, required=False,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    birthDate = serializers.DateField(required=False)
    city = serializers.CharField(required=False)
    mobilePhone = serializers.CharField(required=False)

    def create(self, validated_data):

        user = User.objects.create_user(username=validated_data.get('username'),
                                        email=validated_data.get('username'))
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.set_password(validated_data.get('password'))
        user.save()

        try:
            group = Group.objects.get(name='Staff')
            user.groups.add(group)
            user.save()
            profile = Profile.objects.create(user=user
                                             , gender=validated_data.get('gender'))
            profile.mobilePhone = validated_data.get('mobile_phone')
            profile.address = validated_data.get('address')
            profile.save()
            return profile
        except Exception:
            user.delete()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        pass


class CustomerGetSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    gender = serializers.CharField(required=False)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    username = serializers.CharField(required=False,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    # password = serializers.CharField(write_only=True)
    birthDate = serializers.DateField(required=False)
    city = serializers.CharField(required=False)
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    mobilePhone = serializers.CharField(required=False)
    isCorporate = serializers.BooleanField(required=True)
    taxNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    firmName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    taxOffice = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    actions = serializers.CharField(read_only=True)


class CustomerAddSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    gender = serializers.CharField(required=False)
    firstName = serializers.CharField(required=True, write_only=True)
    lastName = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=False, write_only=True,
                                     )
    # password = serializers.CharField(write_only=True)
    birthDate = serializers.DateField(required=False)
    city = serializers.CharField(required=False)
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    mobilePhone = serializers.CharField(required=False)
    isCorporate = serializers.BooleanField(required=True)
    taxNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    firmName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    taxOffice = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    actions = serializers.CharField(read_only=True)
    isSendMail = serializers.BooleanField(read_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(username=validated_data.get('username'),
                                        email=validated_data.get('username'))
        user.first_name = validated_data.get("firstName")
        user.last_name = validated_data.get("lastName")
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        try:
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.mobilePhone = validated_data.get('mobilePhone')
            profile.address = validated_data.get('address')

            if validated_data.get('isCorporate'):
                profile.taxNumber = validated_data.get('taxNumber')
                profile.firmName = validated_data.get('firmName')
                profile.taxOffice = validated_data.get('taxOffice')
                profile.isCorporate = True

            else:
                profile.isCorporate = False

            profile.save()
            # MailServices.send_password(password=password, to=user.email)
            return profile
        except Exception:
            user.delete()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:
            user = instance.user
            user.first_name = validated_data.get("firstName")
            user.last_name = validated_data.get("lastName")
            user.username = validated_data.get("username")
            user.email = validated_data.get("username")
            instance.mobilePhone = validated_data.get('mobilePhone')
            instance.address = validated_data.get('address')

            if validated_data.get('isCorporate'):
                instance.taxNumber = validated_data.get('taxNumber')
                instance.firmName = validated_data.get('firmName')
                instance.taxOffice = validated_data.get('taxOffice')
                instance.isCorporate = True

            else:
                instance.isCorporate = False

            user.save()
            instance.save()

            return instance

        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class CustomerPageSerializer(serializers.Serializer):
    data = CustomerAddSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()


class StaffSingleSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    gender = serializers.CharField(required=False)
    firstName = serializers.CharField(required=True, allow_blank=False)
    lastName = serializers.CharField(required=True, allow_blank=False)
    username = serializers.CharField(required=False,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    # password = serializers.CharField(write_only=True)

    mobilePhone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    actions = serializers.CharField(read_only=True)
    group = serializers.CharField(read_only=True, label="grup")
    address = serializers.CharField(allow_null=True, required=False, allow_blank=True)


class StaffSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    gender = serializers.CharField(required=False)
    firstName = serializers.CharField(required=True, write_only=True, allow_blank=False)
    lastName = serializers.CharField(required=True, write_only=True, allow_blank=False)
    username = serializers.CharField(write_only=True, required=False,
                                     )
    # password = serializers.CharField(write_only=True)

    mobilePhone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    actions = serializers.CharField(read_only=True)
    group = serializers.CharField(write_only=True, label="grup")
    address = serializers.CharField(allow_null=True, required=False, allow_blank=True)

    def create(self, validated_data):

        user = User.objects.create_user(username=validated_data.get('username'),
                                        email=validated_data.get('username'))
        email = user.email
        password = User.objects.make_random_password()
        user.first_name = validated_data.get("firstName")
        user.last_name = validated_data.get("lastName")
        user.set_password(password)
        user.save()

        try:
            group = Group.objects.get(id=int(validated_data.get("group")))
            user.groups.add(group)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.mobilePhone = validated_data.get('mobilePhone')
            profile.address = validated_data.get('address')
            profile.save()
            MailServices.send_password(password=password, to=user.email)
            return profile
        except Exception:
            traceback.print_exc()
            user.delete()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:
            user = instance.user
            user.first_name = validated_data.get("firstName")
            user.last_name = validated_data.get("lastName")
            user.username = validated_data.get("username")
            user.email = validated_data.get("username")
            instance.mobilePhone = validated_data.get('mobilePhone')
            instance.address = validated_data.get('address')
            user.groups.clear()
            user.groups.add(Group.objects.get(id=int(validated_data.get("group"))))

            user.save()
            instance.save()

            return instance

        except Exception:

            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StaffPageSerializer(serializers.Serializer):
    data = StaffSerializer(many=True)
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
