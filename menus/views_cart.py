from rest_framework import generics, viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from menus.models import Cart
from menus import serializers
from users.permissions.role_permissions import RolePermission
from users.permissions.user_permissions import UserPermission


class CartListOrCreateAPIViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    list_serializer_class = serializers.CartListSerializer
    create_serializer_class = serializers.CartCreateSerializer
    permission_classes = [UserPermission]
    perm_slug = ""

    def list(self, request, *args, **kwargs):
        try:
            if request.user.role.slug in [""]:
                serializer = self.list_serializer_class(self.queryset, many=True)
                return Response(serializer.data)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except AttributeError:
            serializer = self.list_serializer_class(self.queryset, many=True)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            if request.user.role.slug in [""]:
                serializer = self.create_serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise APIException("No permission")
        except AttributeError:
            raise APIException("No permission")


class CartRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartDeleteSerializer
    perm_slug = "menus.cart"
    #permission_classes = [UserPermission]

    def retrieve(self, request, *args, **kwargs):
        try:
            if request.user.role.slug:
                raise APIException("You do not have Authorization")
        except AttributeError:
            queryset = self.queryset.first()
            serializer = serializers.CartDetailSerializer(queryset)
            return Response(serializer.data)



