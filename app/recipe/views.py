from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient
from recipe import serializers


class BaseRecipeAttrViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """Base viewset for user owned recipe attributes

    Args:
        viewsets ([type]): [description]
        mixins ([type]): [description]
        mixins ([type]): [description]
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """Create a new object

        Args:
            serializer ([type]): [description]
        """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


# Refactor bcs they are very similar
# class TagViewSet(
#     viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
# ):
#     """Manage tag in the database

#     Args:
#         viewsets ([type]): [description]
#         mixins ([type]): [description]
#     """

#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer

#     def get_queryset(self):
#         """Return objects for the current authenticated user only

#         Returns:
#             [type]: [description]
#         """
#         return self.queryset.filter(user=self.request.user).order_by("-name")

#     def perform_create(self, serializer):
#         """Create a new tag

#         Args:
#             serializer ([type]): [description]
#         """
#         serializer.save(user=self.request.user)


# class IngredientViewSet(
#     viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
# ):
#     """Manage ingredients in the database

#     Args:
#         viewsets ([type]): [description]
#         mixins ([type]): [description]
#     """

#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Ingredient.objects.all()
#     serializer_class = serializers.IngredientSerializer

#     def get_queryset(self):
#         """Return objects for the current authenticated user"""
#         return self.queryset.filter(user=self.request.user).order_by("-name")

#     def perform_create(self, serializer):
#         """Create a new ingredient"""
#         serializer.save(user=self.request.user)
