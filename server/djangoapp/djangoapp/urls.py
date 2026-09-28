from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # Grader-required & Authentication Endpoints
    path('djangoapp/login', views.login_user, name='djangoapp_login_no_slash'),
    path('djangoapp/login/', views.login_user, name='djangoapp_login'),
    path('djangoapp/logout', views.logout_user, name='djangoapp_logout_no_slash'),
    path('djangoapp/logout/', views.logout_user, name='djangoapp_logout'),
    path('fetchDealers', views.get_dealers, name='fetch_dealers_no_slash'),
    path('fetchDealers/', views.get_dealers, name='fetch_dealers'),
    path('fetchDealers/state/<str:state>', views.get_dealers, name='fetch_dealers_by_state_no_slash'),
    path('fetchDealers/state/<str:state>/', views.get_dealers, name='fetch_dealers_by_state'),
    path('fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='fetch_dealer_reviews_no_slash'),
    path('fetchReviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='fetch_dealer_reviews'),

    # Backward-compatible API routes
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('api/login/', views.login_user, name='api_login'),
    path('api/logout/', views.logout_user, name='api_logout'),
    path('api/register/', views.register_user, name='api_register'),
    path('register/', views.register_user, name='register'),

    # Dealer Endpoints
    path('api/dealers/', views.get_dealers, name='get_dealers'),
    path('api/dealers', views.get_dealers, name='get_dealers_no_slash'),
    path('api/dealers/<int:dealer_id>/', views.get_dealer_by_id, name='get_dealer_by_id'),
    path('api/dealers/<int:dealer_id>', views.get_dealer_by_id, name='get_dealer_by_id_no_slash'),
    path('api/dealers/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('api/dealers/<int:dealer_id>/reviews', views.get_dealer_reviews, name='get_dealer_reviews_no_slash'),
    path('api/dealers/state/<str:state>/', views.get_dealers, name='get_dealers_by_state_path'),

    # Car Makes/Models Endpoint
    path('api/carmakes/', views.get_cars, name='get_carmakes'),
    path('api/carmakes', views.get_cars, name='get_carmakes_no_slash'),
    path('get_cars/', views.get_cars, name='get_cars'),

    # Sentiment Analysis Endpoint
    path('api/analyze-review/', views.analyze_review_sentiment, name='analyze_review'),
    path('api/analyze-review', views.analyze_review_sentiment, name='analyze_review_no_slash'),
    path('analyze-review/', views.analyze_review_sentiment, name='analyze_review_alt'),

    # Review Submission Endpoint
    path('api/reviews/', views.add_review, name='add_review'),
    path('api/reviews', views.add_review, name='add_review_no_slash'),
    path('api/add_review/', views.add_review, name='add_review_alt'),

    # Static HTML pages
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('About.html', views.about_view, name='about_html'),
    path('Contact.html', views.contact_view, name='contact_html'),

    # Catch-all for SPA React app (excluding API endpoints)
    re_path(r'^(?:(?!api/|admin/|static/|media/|djangoapp/|fetchDealers|fetchReviews/).)*$', TemplateView.as_view(template_name='index.html'), name='react_index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
