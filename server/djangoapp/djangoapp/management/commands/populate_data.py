from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from djangoapp.models import CarMake, CarModel, Dealer, Review

class Command(BaseCommand):
    help = 'Populates the database with realistic sample dealers, car makes/models, and reviews.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating sample database data...'))

        # 1. Create Superuser / Admin if not exists
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created (password: admin123).'))
        else:
            admin_user = User.objects.get(username='admin')

        # 2. Create Demo User
        if not User.objects.filter(username='john_doe').exists():
            demo_user = User.objects.create_user('john_doe', 'john@example.com', 'Password123!', first_name='John', last_name='Doe')
            self.stdout.write(self.style.SUCCESS('Demo user "john_doe" created.'))
        else:
            demo_user = User.objects.get(username='john_doe')

        # 3. Create Car Makes & Models
        car_data = [
            {
                'make': 'Toyota',
                'description': 'Reliable and durable Japanese vehicles.',
                'country': 'Japan',
                'models': [
                    {'name': 'Camry', 'type': 'SEDAN', 'year': 2023},
                    {'name': 'RAV4', 'type': 'SUV', 'year': 2024},
                    {'name': 'Highlander', 'type': 'SUV', 'year': 2022},
                    {'name': 'Corolla', 'type': 'SEDAN', 'year': 2023},
                ]
            },
            {
                'make': 'Ford',
                'description': 'American built tough trucks, SUVs, and sedans.',
                'country': 'USA',
                'models': [
                    {'name': 'F-150', 'type': 'TRUCK', 'year': 2024},
                    {'name': 'Explorer', 'type': 'SUV', 'year': 2023},
                    {'name': 'Mustang', 'type': 'COUPE', 'year': 2022},
                    {'name': 'Escape', 'type': 'SUV', 'year': 2023},
                ]
            },
            {
                'make': 'Honda',
                'description': 'Innovative engineering and fuel-efficient cars.',
                'country': 'Japan',
                'models': [
                    {'name': 'Civic', 'type': 'SEDAN', 'year': 2023},
                    {'name': 'CR-V', 'type': 'SUV', 'year': 2024},
                    {'name': 'Accord', 'type': 'SEDAN', 'year': 2023},
                    {'name': 'Pilot', 'type': 'SUV', 'year': 2022},
                ]
            },
            {
                'make': 'Chevrolet',
                'description': 'Classic American brand featuring trucks, SUVs, and sports cars.',
                'country': 'USA',
                'models': [
                    {'name': 'Silverado', 'type': 'TRUCK', 'year': 2024},
                    {'name': 'Tahoe', 'type': 'SUV', 'year': 2023},
                    {'name': 'Malibu', 'type': 'SEDAN', 'year': 2022},
                ]
            },
            {
                'make': 'BMW',
                'description': 'German precision engineering and ultimate driving machines.',
                'country': 'Germany',
                'models': [
                    {'name': '3 Series', 'type': 'SEDAN', 'year': 2023},
                    {'name': 'X5', 'type': 'SUV', 'year': 2024},
                    {'name': 'M4', 'type': 'COUPE', 'year': 2023},
                ]
            }
        ]

        for cdata in car_data:
            make_obj, created = CarMake.objects.get_or_create(
                name=cdata['make'],
                defaults={'description': cdata['description'], 'country': cdata['country']}
            )
            for mdata in cdata['models']:
                CarModel.objects.get_or_create(
                    car_make=make_obj,
                    name=mdata['name'],
                    type=mdata['type'],
                    year=mdata['year']
                )

        self.stdout.write(self.style.SUCCESS('Car Makes and Models populated.'))

        # 4. Create Dealers (including several Kansas dealers!)
        dealers_data = [
            {
                'dealer_id': 1,
                'full_name': 'Midwest Auto World',
                'short_name': 'Midwest Auto',
                'city': 'Wichita',
                'state': 'Kansas',
                'address': '1020 N West St',
                'zip': '67203',
                'lat': 37.6983,
                'long': -97.3912,
                'phone': '(316) 555-0199'
            },
            {
                'dealer_id': 2,
                'full_name': 'Sunflower State Motors',
                'short_name': 'Sunflower Motors',
                'city': 'Topeka',
                'state': 'Kansas',
                'address': '2800 SW Fairlawn Rd',
                'zip': '66614',
                'lat': 39.0256,
                'long': -95.7483,
                'phone': '(785) 555-0144'
            },
            {
                'dealer_id': 3,
                'full_name': 'Overland Park Luxury Cars',
                'short_name': 'Overland Park Dealership',
                'city': 'Overland Park',
                'state': 'Kansas',
                'address': '8700 Metcalf Ave',
                'zip': '66212',
                'lat': 38.9712,
                'long': -94.6708,
                'phone': '(913) 555-0177'
            },
            {
                'dealer_id': 4,
                'full_name': 'Lone Star Ford & Chevy',
                'short_name': 'Lone Star Motors',
                'city': 'Dallas',
                'state': 'Texas',
                'address': '4500 LBJ Freeway',
                'zip': '75244',
                'lat': 32.9234,
                'long': -96.8234,
                'phone': '(214) 555-0188'
            },
            {
                'dealer_id': 5,
                'full_name': 'Pacific Coast Auto Gallery',
                'short_name': 'Pacific Coast',
                'city': 'Los Angeles',
                'state': 'California',
                'address': '10800 Wilshire Blvd',
                'zip': '90024',
                'lat': 34.0583,
                'long': -118.4412,
                'phone': '(310) 555-0122'
            },
            {
                'dealer_id': 6,
                'full_name': 'Empire State Chrysler & Dodge',
                'short_name': 'Empire Motors',
                'city': 'Buffalo',
                'state': 'New York',
                'address': '1500 Main St',
                'zip': '14209',
                'lat': 42.9102,
                'long': -78.8654,
                'phone': '(716) 555-0133'
            }
        ]

        for ddata in dealers_data:
            Dealer.objects.update_or_create(
                dealer_id=ddata['dealer_id'],
                defaults=ddata
            )

        self.stdout.write(self.style.SUCCESS('Dealers populated.'))

        # 5. Create Reviews
        reviews_data = [
            {
                'dealer_id': 1,
                'name': 'Sarah Jenkins',
                'review': 'Fantastic services! The sales agent was extremely helpful and transparent about pricing.',
                'purchase': True,
                'purchase_date': '2023-11-15',
                'car_make': 'Toyota',
                'car_model': 'RAV4',
                'car_year': 2024,
                'sentiment': 'positive',
                'rating': 5
            },
            {
                'dealer_id': 1,
                'name': 'Robert Smith',
                'review': 'Great inventory and clean dealership environment. Very satisfied with my new Camry.',
                'purchase': True,
                'purchase_date': '2023-12-01',
                'car_make': 'Toyota',
                'car_model': 'Camry',
                'car_year': 2023,
                'sentiment': 'positive',
                'rating': 5
            },
            {
                'dealer_id': 2,
                'name': 'Emily Davis',
                'review': 'Decent selection of vehicles. The financing process took longer than expected though.',
                'purchase': False,
                'purchase_date': None,
                'car_make': 'Honda',
                'car_model': 'CR-V',
                'car_year': 2024,
                'sentiment': 'neutral',
                'rating': 3
            },
            {
                'dealer_id': 3,
                'name': 'Michael Johnson',
                'review': 'Top tier customer support! They gave me an amazing trade-in value for my old car.',
                'purchase': True,
                'purchase_date': '2024-01-10',
                'car_make': 'BMW',
                'car_model': 'X5',
                'car_year': 2024,
                'sentiment': 'positive',
                'rating': 5
            },
            {
                'dealer_id': 4,
                'name': 'Carlos Gomez',
                'review': 'Smooth buying experience, no pushy salespeople. Highly recommend Lone Star Motors!',
                'purchase': True,
                'purchase_date': '2024-02-14',
                'car_make': 'Ford',
                'car_model': 'F-150',
                'car_year': 2024,
                'sentiment': 'positive',
                'rating': 5
            }
        ]

        for rdata in reviews_data:
            dealer_obj = Dealer.objects.get(dealer_id=rdata['dealer_id'])
            Review.objects.get_or_create(
                dealer=dealer_obj,
                name=rdata['name'],
                review=rdata['review'],
                defaults={
                    'user': demo_user if rdata['name'] == 'John Doe' else None,
                    'purchase': rdata['purchase'],
                    'purchase_date': rdata['purchase_date'],
                    'car_make': rdata['car_make'],
                    'car_model': rdata['car_model'],
                    'car_year': rdata['car_year'],
                    'sentiment': rdata['sentiment'],
                    'rating': rdata['rating']
                }
            )

        self.stdout.write(self.style.SUCCESS('Reviews populated successfully.'))
