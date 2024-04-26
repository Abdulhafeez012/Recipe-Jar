import uuid
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from apps.user_auth.models import RecipeJarUser
from django.contrib.auth.models import User
from apps.user_auth.serializer import RecipeUserSerializer
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class RecipeUserAPI(ViewSet):
    """
    API endpoint that allows to create a new user or get token.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RecipeUserSerializer

    @action(methods=['post'], detail=False, url_path='create-user', url_name='create_user')
    def post(self, request, *args, **kwargs) -> Response:
        user_uuid = uuid.uuid4()
        user = User.objects.create_user(
            username=user_uuid,
            password=user_uuid.bytes
        )
        serializer = self.serializer_class(data={
            'django_user': user.id,
            'user_id': str(user_uuid),
            'date_of_birth': None,
            'weight': None,
            'height': None
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=False, url_path='delete-user', url_name='delete_user', permission_classes=[permissions.IsAuthenticated])
    def delete(self, request, *args, **kwargs) -> Response:
        data = request.data
        user_id = data.get('user_id')
        user = get_object_or_404(
            RecipeJarUser,
            user_id=user_id
        )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path='get-token', url_name='get_token')
    def get(self, request, *args, **kwargs) -> Response:
        data = request.GET
        user_id = data.get('user_id')
        user = get_object_or_404(
            RecipeJarUser,
            user_id=user_id
        )
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='check-user', url_name='check_user')
    def check_user(self, request, *args, **kwargs) -> Response:
        data = request.GET
        user_id = data.get('user_id')
        try:
            RecipeJarUser.objects.filter(
                user_id=user_id
            )
            return Response(
                {
                    'is_exists': True
                },
                status=status.HTTP_200_OK
            )
        except RecipeJarUser.DoesNotExist:
            return Response(
                {
                    'is_exists': False
                },
                status=status.HTTP_200_OK
            )

