from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    country = models.CharField(max_length=100, default='USA')

    def __str__(self):
        return self.name

class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('TRUCK', 'Truck'),
        ('HATCHBACK', 'Hatchback'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
    ]
    
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField(
        default=2023,
        validators=[
            MinValueValidator(2010),
            MaxValueValidator(2030)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"

class Dealer(models.Model):
    dealer_id = models.IntegerField(unique=True)
    full_name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=50, blank=True, default='')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=20)
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)
    phone = models.CharField(max_length=30, blank=True, default='')

    def __str__(self):
        return f"{self.full_name} ({self.state})"

class Review(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, blank=True, default='')
    car_model = models.CharField(max_length=100, blank=True, default='')
    car_year = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, default='neutral')
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.dealer.full_name} by {self.name}"
