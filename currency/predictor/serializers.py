from rest_framework import serializers

from predictor.models import Exchange


class ExchangeMessageSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        for goal, rate in validated_data['rates'].items():
            Exchange.objects.update_or_create(
                base=validated_data['base'],
                date=validated_data['date'],
                goal=goal,
                rate=rate
            )
        return validated_data

    base = serializers.CharField(max_length=3)
    date = serializers.DateField(input_formats=['iso-8601', '%d-%m-%Y'])
    rates = serializers.DictField(
        child=serializers.DecimalField(decimal_places=6, max_digits=14)
    )


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'
