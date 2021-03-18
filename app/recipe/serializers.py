from core.models import Ingredient, Recipe, Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects

    Args:
        serializers ([type]): [description]
    """

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects

    Args:
        serializers ([type]): [description]
    """

    class Meta:
        model = Ingredient
        fields = ("id", "name")
        read_only_fields = ("id",)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects

    Args:
        serializer ([type]): [description]
    """

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "ingredients",
            "tags",
            "time_minutes",
            "price",
            "link",
        )
        read_only_fields = ("id",)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail

    Args:
        RecipeSerializer ([type]): [description]
    """

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes

    Args:
        serializers ([type]): [description]
    """

    class Meta:
        model = Recipe
        fields = ("id", "image")
        read_only_fields = ("id",)
