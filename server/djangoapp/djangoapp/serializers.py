from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CarMake, CarModel, Dealer, Review

class CarModelSerializer(serializers.ModelSerializer):
    make_name = serializers.CharField(source='car_make.name', read_only=True)
    
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'type', 'year', 'make_name']

class CarMakeSerializer(serializers.ModelSerializer):
    models = CarModelSerializer(many=True, read_only=True)
    
    class Meta:
        model = CarMake
        fields = ['id', 'name', 'description', 'country', 'models']

class DealerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='dealer_id', read_only=True)

    class Meta:
        model = Dealer
        fields = [
            'id', 'dealer_id', 'full_name', 'short_name',
            'city', 'state', 'address', 'zip', 'lat', 'long', 'phone'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    dealer_id = serializers.IntegerField(source='dealer.dealer_id', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'dealer_id', 'name', 'review', 'purchase',
            'purchase_date', 'car_make', 'car_model', 'car_year',
            'sentiment', 'rating', 'created_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
