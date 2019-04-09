from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import *
from rest_framework.decorators import action

from .models import User
from .serializers import *


class UserViewSet(ModelViewSet):
    """
    Checks email and password and returns an auth token.
    """
    permission_classes = ()
    http_method_names = ['post', 'head']
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):

        if request.data["password"] != request.data["passwordConfirmation"]:
            return Response({'register': False, "message": "Password mismatch"})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()

        return Response({'register': self.get_serializer(new_user).data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        """
        Captures the response from the Oauth and checks with the user status.
        """
        # Create a http request for TokenView class(https://github.com/encode/django-rest-framework/issues/2768)
        data = request.data
        queryset = User.objects.filter(username=data['username'], password=data['password'])

        if queryset:
            return Response({'Login': True}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'Login': False}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):

        user = self.get_object()

        if request.data["password"] != request.data["passwordConfirmation"]:
            return Response({'register': False, "message": "Password mismatch"})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_user = User.objects.updata_or_create(id=user.id, defaults=serializer.data)

        return Response({'register': self.get_serializer(updated_user).data}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def resetpassword(self, request, *args, **kwargs):

        user = self.get_object()        
        
        if request.data["password"] != request.data["passwordConfirmation"]:
            user.set_password(request.data["password"])
            user.save()
            return Response({'message': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Password reset link expired. Kindly reset again'},
                            status=status.HTTP_400_BAD_REQUEST)


# class CurrentUserViewSet(mixins.ListModelMixin, GenericViewSet):
#     """
#     Returns the current logged in user details
#     """
#     permission_classes = []
#     serializer_class = UserSerializer
#
#     def list(self, request, *args, **kwargs):
#         return Response(self.serializer_class(self.request.user).data)





