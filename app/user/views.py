from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system

    Args:
        generics ([type]): [description]
    """

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user

    Args:
        ObtainAuthToken ([type]): [description]
    """

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user

    Args:
        generics ([type]): [description]
    """

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return autheticated user

        Returns:
            [type]: [description]
        """
        return self.request.user
