from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import *
# from rest_framework.decorators import action

from .models import Transactions
from .serializers import *
from utils.permissions import BasicPermission


class TransactionViewSet(ModelViewSet):
    """
    Checks email and password and returns an auth token.
    """
    permission_classes = [BasicPermission]
    http_method_names = ['get', 'post', 'head']
    serializer_class = TransactionSerializer

    def list(self, request, *args, **kwargs):

        queryset = Transactions.objects.filter(user=request.user)
        return Response(self.get_serializer(queryset, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        queryset = Transactions.objects.filter(user=request.user)
        return Response({'register': self.get_serializer(queryset).data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):

        record = self.get_object()
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Transactions.objects.updata_or_create(id=record.id, default=serializer.data)
        queryset = Transactions.objects.filter(user=request.user)
        return Response({'register': self.get_serializer(queryset).data}, status=status.HTTP_201_CREATED)
