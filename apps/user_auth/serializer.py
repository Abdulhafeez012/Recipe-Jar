from rest_framework import serializers
from apps.user_auth.models import RecipeJarUser
from rest_framework.authtoken.models import Token


class RecipeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeJarUser
        fields = [
            'django_user',
            'user_id',
            'date_of_birth',
            'weight',
            'height',
        ]

    def create(self, validated_data):
        user = RecipeJarUser.objects.create(
            django_user=validated_data['django_user'],
            user_id=validated_data['user_id'],
            date_of_birth=validated_data['date_of_birth'],
            weight=validated_data['weight'],
            height=validated_data['height']
        )
        token, created = Token.objects.get_or_create(user=user.django_user)
        return user

    def get_token(self, obj):
        token = Token.objects.get(user=obj.django_user)
        return token.key

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('django_user', None)
        response.pop('date_of_birth', None)
        response.pop('weight', None)
        response.pop('height', None)
        response['user_id'] = instance.user_id
        response['token'] = self.get_token(instance)
        return response

