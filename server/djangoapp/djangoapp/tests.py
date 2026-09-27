import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from djangoapp.models import CarMake, CarModel, Dealer, Review

class CarDealershipAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test superuser
        self.admin = User.objects.create_superuser('admin_test', 'admin@test.com', 'AdminPass123!')
        
        # Create test car make & model
        self.make = CarMake.objects.create(name='Toyota', description='Japanese automaker', country='Japan')
        self.model = CarModel.objects.create(car_make=self.make, name='Camry', type='SEDAN', year=2023)
        
        # Create test dealers (including Kansas dealer)
        self.dealer_kansas = Dealer.objects.create(
            dealer_id=101,
            full_name='Kansas City Motors',
            short_name='KC Motors',
            city='Wichita',
            state='Kansas',
            address='100 Main St',
            zip='67201',
            lat=37.68,
            long=-97.33,
            phone='(316) 555-0100'
        )
        self.dealer_texas = Dealer.objects.create(
            dealer_id=102,
            full_name='Austin Auto Hub',
            short_name='Austin Auto',
            city='Austin',
            state='Texas',
            address='200 Congress Ave',
            zip='78701',
            lat=30.26,
            long=-97.74,
            phone='(512) 555-0200'
        )

        # Create test review
        self.review = Review.objects.create(
            dealer=self.dealer_kansas,
            name='Test Reviewer',
            review='Fantastic services and great dealership experience!',
            purchase=True,
            purchase_date='2023-10-01',
            car_make='Toyota',
            car_model='Camry',
            car_year=2023,
            sentiment='positive',
            rating=5
        )

    def test_get_all_dealers(self):
        """Task 9: Retrieve all dealers"""
        response = self.client.get('/api/dealers/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_get_dealer_by_id(self):
        """Task 10: Retrieve dealer by ID"""
        response = self.client.get('/api/dealers/101/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['full_name'], 'Kansas City Motors')

    def test_get_dealers_by_state(self):
        """Task 11: Filter dealers by state (Kansas)"""
        response = self.client.get('/api/dealers/?state=Kansas')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(all(d['state'].lower() == 'kansas' for d in data))

    def test_get_dealer_reviews(self):
        """Task 8: Retrieve dealer reviews"""
        response = self.client.get('/api/dealers/101/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Reviewer')

    def test_get_carmakes(self):
        """Tasks 14 & 15: Retrieve car makes and models"""
        response = self.client.get('/api/carmakes/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('CarMakes', data)
        self.assertGreaterEqual(len(data['CarMakes']), 1)

    def test_analyze_review_sentiment(self):
        """Task 16: Analyze sentiment"""
        response = self.client.post(
            '/api/analyze-review/',
            data=json.dumps({'text': 'Fantastic services'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['sentiment'], 'positive')

    def test_user_registration_and_login_logout(self):
        """Tasks 5, 6, 7: Registration, Login, Logout"""
        # Register
        reg_resp = self.client.post(
            '/api/register/',
            data=json.dumps({
                'username': 'newuser',
                'firstName': 'New',
                'lastName': 'User',
                'email': 'newuser@example.com',
                'password': 'Password123!'
            }),
            content_type='application/json'
        )
        self.assertEqual(reg_resp.status_code, 201)
        self.assertEqual(reg_resp.json()['status'], 'Authenticated')

        # Logout
        logout_resp = self.client.post('/api/logout/')
        self.assertEqual(logout_resp.status_code, 200)
        self.assertEqual(logout_resp.json()['status'], 'Logged out')

        # Login
        login_resp = self.client.post(
            '/api/login/',
            data=json.dumps({'userName': 'newuser', 'password': 'Password123!'}),
            content_type='application/json'
        )
        self.assertEqual(login_resp.status_code, 200)
        self.assertEqual(login_resp.json()['status'], 'Authenticated')

    def test_add_review(self):
        """Task 22: Add review for a dealer"""
        response = self.client.post(
            '/api/reviews/',
            data=json.dumps({
                'dealer_id': 101,
                'name': 'Customer One',
                'review': 'Excellent customer service and easy transaction.',
                'rating': 5,
                'purchase': True,
                'purchase_date': '2023-11-20',
                'car_make': 'Toyota',
                'car_model': 'Camry',
                'car_year': 2023
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['sentiment'], 'positive')
