from core.models import Ingredient, Recipe, Tag
from recipe import serializers
from rest_framework import mixins, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


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


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database

    Args:
        viewsets ([type]): [description]
    """

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string iD to a list on integers

        Args:
            qs ([type]): [description]
        """
        return [int(x) for x in qs.split(",")]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        tags = self.request.query_params.get("tags")
        ingredients = self.request.query_params.get("ingredients")
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":
            return serializers.RecipeDetailSerializer
        # Can't made it upload-image no fucking idea how to
        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe

        Args:
            serializer ([type]): [description]
        """
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        name="upload-image",
        url_name="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Upload image to a recipe

        Args:
            request ([type]): [description]
            pk ([type], optional): [description]. Defaults to None.
        """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
