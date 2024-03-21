from rest_framework import serializers
from apps.user_auth.models import RecipeJarUser
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]
