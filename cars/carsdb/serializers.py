from rest_framework import serializers

from carsdb.models import parts


class PartSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = parts
        fields = (
            'id',
            'type',
            'model_p',
            'price',
            'count_p',
            'params',
            'author',
        )
        read_only_fields = ('id', 'author')

    def validate_price(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError('Price must be greater than zero.')
        return value

    def validate_count_p(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError('Quantity must be greater than zero.')
        return value
