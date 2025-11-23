from rest_framework import serializers
from test_app.models import Category

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category with such name already exists")
        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        unique_name = validated_data.get('name', instance.name)

        if Category.objects.filter(name=unique_name).exclude(id=instance.id).exists():
            raise serializers.ValidationError("Category with such name already exists")

        instance.name = unique_name
        instance.save()
        return instance

