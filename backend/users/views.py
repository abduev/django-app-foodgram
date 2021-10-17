from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import Subscription
from api.serializers import SubscribeSerializer


User = get_user_model()


class UserCustomViewSet(UserViewSet):
    lookup_field = 'pk'
    permission_classes = (AllowAny,)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request, *args, **kwargs):
        """Authenticated user's subscriptions to authors"""
        subscribes = User.objects.filter(
            subscribing__user=self.request.user
        )
        serializer = SubscribeSerializer(
            subscribes, context={'request': request}, many=True
        )
        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(page)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk):
        """Authenticated user subscribes to author(pk)"""
        user = self.request.user
        author = get_object_or_404(User, pk=pk)
        serializer = SubscribeSerializer(author, context={'request': request})
        if request.method == 'DELETE':
            Subscription.objects.filter(
                user=user, author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if user == author:
            raise ValidationError(
                {'errors': 'Subscribing to yourself is not allowed!'}
            )
        elif not Subscription.objects.filter(
            user=user, author=author
        ).exists():
            Subscription.objects.create(user=user, author=author)
            serializer = SubscribeSerializer(
                author, context={'request': request}
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        raise ValidationError(
            {'errors': 'The subscription is already exist!'}
        )
