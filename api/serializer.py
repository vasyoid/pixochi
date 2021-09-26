from rest_framework import serializers


class NewPixochiRequestSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=10)
    eyes = serializers.IntegerField()
    filling = serializers.CharField(min_length=1, max_length=1)

    def validate_eyes(self, value):
        if value < 1:
            raise serializers.ValidationError("Pixochi must have at least one eye")
        if value > 8:
            raise serializers.ValidationError("Pixochi can't have more than 8 eyes")
        return value


class PixochiStateResponseSerializer(serializers.Serializer):
    state = serializers.CharField()
    pic = serializers.CharField()
