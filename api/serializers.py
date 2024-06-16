from rest_framework import serializers
from .models import Color, Person

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    color_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = "__all__"

    def get_color_info(self, obj):
        color_obj = Color.objects.get(id = obj.color.id)
        return {"color_name":color_obj.color_name}

    def validate_no(self, no):
        if no > 500:
            raise serializers.ValidationError('no should be less than or equal to 500')
        return no
