import json
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .models import CarMake, CarModel, Dealer, Review
from .serializers import (
    CarMakeSerializer, CarModelSerializer, DealerSerializer,
    ReviewSerializer, UserSerializer
)

vader_analyzer = SentimentIntensityAnalyzer()

def analyze_text_sentiment(text):
    """
    Helper function to perform sentiment analysis using Flask microservice
    or local vaderSentiment fallback.
    """
    if not text:
        return "neutral"
    
    # Try calling external/local Flask microservice on port 5000 first
    try:
        response = requests.post(
            'http://127.0.0.1:5000/analyze',
            json={'text': text},
            timeout=1.5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('sentiment', 'neutral')
    except Exception:
        pass # Fallback to local vaderSentiment if Flask microservice is not reachable

    # Local fallback using vaderSentiment
    scores = vader_analyzer.polarity_scores(text)
    compound = scores.get('compound', 0)
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"

@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def login_user(request):
    """
    Endpoint for user authentication. Accepts JSON or form data.
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return JsonResponse({'status': 'Authenticated', 'userName': request.user.username})
        return JsonResponse({'status': 'Not Authenticated', 'userName': ''})

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    username = data.get('userName') or data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password required', 'status': 'Failed'}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            'userName': user.username,
            'status': 'Authenticated',
            'message': 'Login successful'
        })
    else:
        return JsonResponse({
            'status': 'Failed',
            'error': 'Invalid credentials'
        }, status=401)

@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def logout_user(request):
    """
    Endpoint for user logout.
    """
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({
        'status': 'Logged out',
        'userName': username,
        'message': 'Successfully logged out'
    })

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Endpoint for user registration. Expects: username, first_name, last_name, email, password.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    username = data.get('username') or data.get('userName')
    first_name = data.get('firstName') or data.get('first_name', '')
    last_name = data.get('lastName') or data.get('last_name', '')
    email = data.get('email', '')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists', 'status': 'Failed'}, status=400)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    user.save()
    login(request, user)

    return JsonResponse({
        'status': 'Authenticated',
        'userName': user.username,
        'message': 'Registration successful'
    }, status=201)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_dealers(request, state=None):
    """
    Endpoint to retrieve all dealers or filter dealers by state.
    Supports query parameter: ?state=Kansas
    """
    query_state = state or request.GET.get('state')
    if query_state:
        dealers = Dealer.objects.filter(state__iexact=query_state)
    else:
        dealers = Dealer.objects.all()

    serializer = DealerSerializer(dealers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_dealer_by_id(request, dealer_id):
    """
    Endpoint to retrieve single dealer details by dealer_id.
    """
    try:
        dealer = Dealer.objects.get(dealer_id=dealer_id)
        serializer = DealerSerializer(dealer)
        return Response(serializer.data)
    except Dealer.DoesNotExist:
        return Response({'error': f'Dealer with ID {dealer_id} not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_dealer_reviews(request, dealer_id):
    """
    Endpoint to retrieve all reviews for a specific dealer_id.
    """
    try:
        dealer = Dealer.objects.get(dealer_id=dealer_id)
    except Dealer.DoesNotExist:
        return Response({'error': f'Dealer with ID {dealer_id} not found'}, status=status.HTTP_404_NOT_FOUND)

    reviews = Review.objects.filter(dealer=dealer)
    
    # Update missing sentiments dynamically
    for rev in reviews:
        if not rev.sentiment or rev.sentiment == 'neutral':
            rev.sentiment = analyze_text_sentiment(rev.review)
            rev.save()

    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_cars(request):
    """
    Endpoint to retrieve all car makes and their associated models.
    """
    car_makes = CarMake.objects.all()
    serializer = CarMakeSerializer(car_makes, many=True)
    return Response({"CarMakes": serializer.data})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_review_sentiment(request):
    """
    Endpoint to analyze sentiment for review text.
    Accepts: {"text": "Fantastic services"}
    Returns: {"text": "Fantastic services", "sentiment": "positive"}
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    text = data.get('text', '') or data.get('review', '')
    if not text:
        return JsonResponse({'error': 'No text provided'}, status=400)

    sentiment = analyze_text_sentiment(text)
    return JsonResponse({
        'text': text,
        'sentiment': sentiment
    })

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def add_review(request):
    """
    Endpoint to submit a review for a dealer.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    dealer_id = data.get('dealer_id') or data.get('dealer')
    review_text = data.get('review') or data.get('review_text') or data.get('content')
    name = data.get('name') or (request.user.username if request.user.is_authenticated else 'Anonymous')
    purchase = data.get('purchase', False)
    if isinstance(purchase, str):
        purchase = purchase.lower() in ['true', '1', 'yes']

    purchase_date = data.get('purchase_date') or None
    if purchase_date == "":
        purchase_date = None

    car_make = data.get('car_make', '')
    car_model = data.get('car_model', '')
    car_year = data.get('car_year') or None
    if car_year == "":
        car_year = None

    rating = data.get('rating', 5)

    if not dealer_id or not review_text:
        return JsonResponse({'error': 'dealer_id and review text are required'}, status=400)

    try:
        dealer = Dealer.objects.get(dealer_id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({'error': f'Dealer {dealer_id} not found'}, status=404)

    sentiment = analyze_text_sentiment(review_text)

    review_obj = Review.objects.create(
        dealer=dealer,
        user=request.user if request.user.is_authenticated else None,
        name=name,
        review=review_text,
        purchase=purchase,
        purchase_date=purchase_date,
        car_make=car_make,
        car_model=car_model,
        car_year=car_year,
        sentiment=sentiment,
        rating=rating
    )

    serializer = ReviewSerializer(review_obj)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def about_view(request):
    return render(request, 'static/About.html')

def contact_view(request):
    return render(request, 'static/Contact.html')
