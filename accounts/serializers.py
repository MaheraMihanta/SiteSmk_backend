from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    entity = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'display_name',
            'first_name',
            'last_name',
            'role',
            'phone',
            'address',
            'is_active',
            'entity',
        ]

    def get_entity(self, obj):
        account = getattr(obj, 'entity_account', None)
        if not account:
            return None
        entity = account.entity
        return {
            'id': entity.id,
            'name': entity.name,
            'city': entity.city,
            'isNationalOffice': entity.is_national_office,
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

