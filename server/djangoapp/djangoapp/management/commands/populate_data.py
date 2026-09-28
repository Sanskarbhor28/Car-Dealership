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
            demo_user.set_password('Password123!')
            demo_user.save()

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

        # 4. Create 50 Dealers
        dealers_data = [
            {'dealer_id': 1, 'full_name': 'Midwest Auto World', 'short_name': 'Midwest Auto', 'city': 'Wichita', 'state': 'Kansas', 'address': '1020 N West St', 'zip': '67203', 'lat': 37.6983, 'long': -97.3912, 'phone': '(316) 555-0199'},
            {'dealer_id': 2, 'full_name': 'Sunflower State Motors', 'short_name': 'Sunflower Motors', 'city': 'Topeka', 'state': 'Kansas', 'address': '2800 SW Fairlawn Rd', 'zip': '66614', 'lat': 39.0256, 'long': -95.7483, 'phone': '(785) 555-0144'},
            {'dealer_id': 3, 'full_name': 'Overland Park Luxury Cars', 'short_name': 'Overland Park Dealership', 'city': 'Overland Park', 'state': 'Kansas', 'address': '8700 Metcalf Ave', 'zip': '66212', 'lat': 38.9712, 'long': -94.6708, 'phone': '(913) 555-0177'},
            {'dealer_id': 4, 'full_name': 'Lone Star Ford & Chevy', 'short_name': 'Lone Star Motors', 'city': 'Dallas', 'state': 'Texas', 'address': '4500 LBJ Freeway', 'zip': '75244', 'lat': 32.9234, 'long': -96.8234, 'phone': '(214) 555-0188'},
            {'dealer_id': 5, 'full_name': 'Pacific Coast Auto Gallery', 'short_name': 'Pacific Coast', 'city': 'Los Angeles', 'state': 'California', 'address': '10800 Wilshire Blvd', 'zip': '90024', 'lat': 34.0583, 'long': -118.4412, 'phone': '(310) 555-0122'},
            {'dealer_id': 6, 'full_name': 'Empire State Chrysler & Dodge', 'short_name': 'Empire Motors', 'city': 'Buffalo', 'state': 'New York', 'address': '1500 Main St', 'zip': '14209', 'lat': 42.9102, 'long': -78.8654, 'phone': '(716) 555-0133'},
            {'dealer_id': 7, 'full_name': 'Sunshine State Auto', 'short_name': 'Sunshine Auto', 'city': 'Miami', 'state': 'Florida', 'address': '7200 Biscayne Blvd', 'zip': '33138', 'lat': 25.8412, 'long': -80.1865, 'phone': '(305) 555-0111'},
            {'dealer_id': 8, 'full_name': 'Peach State Motors', 'short_name': 'Peach State', 'city': 'Atlanta', 'state': 'Georgia', 'address': '3400 Peachtree Rd NE', 'zip': '30326', 'lat': 33.8481, 'long': -84.3642, 'phone': '(404) 555-0122'},
            {'dealer_id': 9, 'full_name': 'Windy City Autos', 'short_name': 'Windy City', 'city': 'Chicago', 'state': 'Illinois', 'address': '2500 N Western Ave', 'zip': '60647', 'lat': 41.9272, 'long': -87.6873, 'phone': '(312) 555-0133'},
            {'dealer_id': 10, 'full_name': 'Great Lakes Dealership', 'short_name': 'Great Lakes', 'city': 'Detroit', 'state': 'Michigan', 'address': '1000 Woodward Ave', 'zip': '48226', 'lat': 42.3314, 'long': -83.0458, 'phone': '(313) 555-0144'},
            {'dealer_id': 11, 'full_name': 'Keystone Motors', 'short_name': 'Keystone', 'city': 'Philadelphia', 'state': 'Pennsylvania', 'address': '1800 Broad St', 'zip': '19145', 'lat': 39.9281, 'long': -75.1692, 'phone': '(215) 555-0155'},
            {'dealer_id': 12, 'full_name': 'Tar Heel Auto Sales', 'short_name': 'Tar Heel Auto', 'city': 'Charlotte', 'state': 'North Carolina', 'address': '400 S Tryon St', 'zip': '28202', 'lat': 35.2253, 'long': -80.8441, 'phone': '(704) 555-0166'},
            {'dealer_id': 13, 'full_name': 'Centennial State Cars', 'short_name': 'Centennial Cars', 'city': 'Denver', 'state': 'Colorado', 'address': '1500 Broadway', 'zip': '80202', 'lat': 39.7401, 'long': -104.9872, 'phone': '(303) 555-0177'},
            {'dealer_id': 14, 'full_name': 'Emerald City Motors', 'short_name': 'Emerald City', 'city': 'Seattle', 'state': 'Washington', 'address': '2000 4th Ave', 'zip': '98121', 'lat': 47.6132, 'long': -122.3412, 'phone': '(206) 555-0188'},
            {'dealer_id': 15, 'full_name': 'Music City Auto Gallery', 'short_name': 'Music City Auto', 'city': 'Nashville', 'state': 'Tennessee', 'address': '1100 Broadway', 'zip': '37203', 'lat': 36.1582, 'long': -86.7842, 'phone': '(615) 555-0199'},
            {'dealer_id': 16, 'full_name': 'Valley of the Sun Motors', 'short_name': 'Valley Sun', 'city': 'Phoenix', 'state': 'Arizona', 'address': '2400 E Camelback Rd', 'zip': '85016', 'lat': 33.5092, 'long': -112.0284, 'phone': '(602) 555-0211'},
            {'dealer_id': 17, 'full_name': 'Bay State Automotive', 'short_name': 'Bay State Auto', 'city': 'Boston', 'state': 'Massachusetts', 'address': '800 Boylston St', 'zip': '02199', 'lat': 42.3472, 'long': -71.0823, 'phone': '(617) 555-0222'},
            {'dealer_id': 18, 'full_name': 'Gateway City Motors', 'short_name': 'Gateway Motors', 'city': 'St. Louis', 'state': 'Missouri', 'address': '500 Market St', 'zip': '63101', 'lat': 38.6261, 'long': -90.1892, 'phone': '(314) 555-0233'},
            {'dealer_id': 19, 'full_name': 'Alamo City Auto', 'short_name': 'Alamo Auto', 'city': 'San Antonio', 'state': 'Texas', 'address': '300 E Houston St', 'zip': '78205', 'lat': 29.4262, 'long': -98.4891, 'phone': '(210) 555-0244'},
            {'dealer_id': 20, 'full_name': 'Twin Cities Motors', 'short_name': 'Twin Cities', 'city': 'Minneapolis', 'state': 'Minnesota', 'address': '700 Nicollet Mall', 'zip': '55402', 'lat': 44.9762, 'long': -93.2721, 'phone': '(612) 555-0255'},
            {'dealer_id': 21, 'full_name': 'Silicon Valley Auto', 'short_name': 'Silicon Auto', 'city': 'San Jose', 'state': 'California', 'address': '100 W San Fernando St', 'zip': '95113', 'lat': 37.3342, 'long': -121.8912, 'phone': '(408) 555-0266'},
            {'dealer_id': 22, 'full_name': 'Charm City Motors', 'short_name': 'Charm City', 'city': 'Baltimore', 'state': 'Maryland', 'address': '200 E Pratt St', 'zip': '21202', 'lat': 39.2872, 'long': -76.6112, 'phone': '(410) 555-0277'},
            {'dealer_id': 23, 'full_name': 'Hoosier State Auto', 'short_name': 'Hoosier Auto', 'city': 'Indianapolis', 'state': 'Indiana', 'address': '1 Monument Cir', 'zip': '46204', 'lat': 39.7684, 'long': -86.1581, 'phone': '(317) 555-0288'},
            {'dealer_id': 24, 'full_name': 'Rose City Motors', 'short_name': 'Rose City', 'city': 'Portland', 'state': 'Oregon', 'address': '1000 SW Broadway', 'zip': '97205', 'lat': 45.5182, 'long': -122.6792, 'phone': '(503) 555-0299'},
            {'dealer_id': 25, 'full_name': 'Queen City Auto', 'short_name': 'Queen City', 'city': 'Cincinnati', 'state': 'Ohio', 'address': '500 Walnut St', 'zip': '45202', 'lat': 39.1022, 'long': -84.5112, 'phone': '(513) 555-0311'},
            {'dealer_id': 26, 'full_name': 'Silver State Motors', 'short_name': 'Silver State', 'city': 'Las Vegas', 'state': 'Nevada', 'address': '3500 Las Vegas Blvd S', 'zip': '89109', 'lat': 36.1172, 'long': -115.1721, 'phone': '(702) 555-0322'},
            {'dealer_id': 27, 'full_name': 'Salt Lake Auto', 'short_name': 'Salt Lake Motors', 'city': 'Salt Lake City', 'state': 'Utah', 'address': '50 S Main St', 'zip': '84101', 'lat': 40.7682, 'long': -111.8912, 'phone': '(801) 555-0333'},
            {'dealer_id': 28, 'full_name': 'Bluegrass Motors', 'short_name': 'Bluegrass Auto', 'city': 'Louisville', 'state': 'Kentucky', 'address': '400 W Market St', 'zip': '40202', 'lat': 38.2562, 'long': -85.7581, 'phone': '(502) 555-0344'},
            {'dealer_id': 29, 'full_name': 'Badger State Auto', 'short_name': 'Badger Auto', 'city': 'Milwaukee', 'state': 'Wisconsin', 'address': '500 E Wisconsin Ave', 'zip': '53202', 'lat': 43.0382, 'long': -87.9041, 'phone': '(414) 555-0355'},
            {'dealer_id': 30, 'full_name': 'Sooner State Motors', 'short_name': 'Sooner Motors', 'city': 'Oklahoma City', 'state': 'Oklahoma', 'address': '100 N Broadway Ave', 'zip': '73102', 'lat': 35.4682, 'long': -97.5161, 'phone': '(405) 555-0366'},
            {'dealer_id': 31, 'full_name': 'Pelican State Auto', 'short_name': 'Pelican Auto', 'city': 'New Orleans', 'state': 'Louisiana', 'address': '600 Canal St', 'zip': '70130', 'lat': 29.9522, 'long': -90.0691, 'phone': '(504) 555-0377'},
            {'dealer_id': 32, 'full_name': 'Monumental Motors', 'short_name': 'Monumental Auto', 'city': 'Washington', 'state': 'District of Columbia', 'address': '1400 Pennsylvania Ave NW', 'zip': '20004', 'lat': 38.8972, 'long': -77.0321, 'phone': '(202) 555-0388'},
            {'dealer_id': 33, 'full_name': 'First State Auto', 'short_name': 'First State', 'city': 'Wilmington', 'state': 'Delaware', 'address': '1000 N Market St', 'zip': '19801', 'lat': 39.7452, 'long': -75.5481, 'phone': '(302) 555-0399'},
            {'dealer_id': 34, 'full_name': 'Green Mountain Motors', 'short_name': 'Green Mountain', 'city': 'Burlington', 'state': 'Vermont', 'address': '100 Church St', 'zip': '05401', 'lat': 44.4762, 'long': -73.2121, 'phone': '(802) 555-0411'},
            {'dealer_id': 35, 'full_name': 'Ocean State Auto', 'short_name': 'Ocean State', 'city': 'Providence', 'state': 'Rhode Island', 'address': '1 Westminster St', 'zip': '02903', 'lat': 41.8242, 'long': -71.4121, 'phone': '(401) 555-0422'},
            {'dealer_id': 36, 'full_name': 'Nutmeg State Motors', 'short_name': 'Nutmeg Motors', 'city': 'Hartford', 'state': 'Connecticut', 'address': '100 Pearl St', 'zip': '06103', 'lat': 41.7662, 'long': -72.6741, 'phone': '(860) 555-0433'},
            {'dealer_id': 37, 'full_name': 'Pine Tree Auto', 'short_name': 'Pine Tree', 'city': 'Portland', 'state': 'Maine', 'address': '400 Congress St', 'zip': '04101', 'lat': 43.6592, 'long': -70.2561, 'phone': '(207) 555-0444'},
            {'dealer_id': 38, 'full_name': 'Granite State Motors', 'short_name': 'Granite Motors', 'city': 'Manchester', 'state': 'New Hampshire', 'address': '1000 Elm St', 'zip': '03101', 'lat': 42.9912, 'long': -71.4631, 'phone': '(603) 555-0455'},
            {'dealer_id': 39, 'full_name': 'Garden State Auto', 'short_name': 'Garden State', 'city': 'Newark', 'state': 'New Jersey', 'address': '50 Park Pl', 'zip': '07102', 'lat': 40.7382, 'long': -74.1681, 'phone': '(973) 555-0466'},
            {'dealer_id': 40, 'full_name': 'Old Dominion Motors', 'short_name': 'Old Dominion', 'city': 'Richmond', 'state': 'Virginia', 'address': '900 E Main St', 'zip': '23219', 'lat': 37.5412, 'long': -77.4341, 'phone': '(804) 555-0477'},
            {'dealer_id': 41, 'full_name': 'Mountain State Auto', 'short_name': 'Mountain State', 'city': 'Charleston', 'state': 'West Virginia', 'address': '500 Virginia St E', 'zip': '25301', 'lat': 38.3492, 'long': -81.6321, 'phone': '(304) 555-0488'},
            {'dealer_id': 42, 'full_name': 'Palmetto State Motors', 'short_name': 'Palmetto Motors', 'city': 'Charleston', 'state': 'South Carolina', 'address': '200 Meeting St', 'zip': '29401', 'lat': 32.7812, 'long': -79.9321, 'phone': '(843) 555-0499'},
            {'dealer_id': 43, 'full_name': 'Magnolia State Auto', 'short_name': 'Magnolia Auto', 'city': 'Jackson', 'state': 'Mississippi', 'address': '100 Capitol St', 'zip': '39201', 'lat': 32.2992, 'long': -90.1821, 'phone': '(601) 555-0511'},
            {'dealer_id': 44, 'full_name': 'Volunteer State Motors', 'short_name': 'Volunteer Motors', 'city': 'Memphis', 'state': 'Tennessee', 'address': '100 Peabody Pl', 'zip': '38103', 'lat': 35.1412, 'long': -90.0521, 'phone': '(901) 555-0522'},
            {'dealer_id': 45, 'full_name': 'Yellowhammer Auto', 'short_name': 'Yellowhammer', 'city': 'Birmingham', 'state': 'Alabama', 'address': '1900 5th Ave N', 'zip': '35203', 'lat': 33.5182, 'long': -86.8112, 'phone': '(205) 555-0533'},
            {'dealer_id': 46, 'full_name': 'Natural State Motors', 'short_name': 'Natural State', 'city': 'Little Rock', 'state': 'Arkansas', 'address': '400 W Capitol Ave', 'zip': '72201', 'lat': 34.7462, 'long': -92.2721, 'phone': '(501) 555-0544'},
            {'dealer_id': 47, 'full_name': 'Cornhusker Auto', 'short_name': 'Cornhusker', 'city': 'Omaha', 'state': 'Nebraska', 'address': '1600 Farnam St', 'zip': '68102', 'lat': 41.2582, 'long': -95.9371, 'phone': '(402) 555-0555'},
            {'dealer_id': 48, 'full_name': 'Mount Rushmore Motors', 'short_name': 'Mount Rushmore', 'city': 'Sioux Falls', 'state': 'South Dakota', 'address': '100 Phillips Ave', 'zip': '57104', 'lat': 43.5482, 'long': -96.7281, 'phone': '(605) 555-0566'},
            {'dealer_id': 49, 'full_name': 'Peace Garden Auto', 'short_name': 'Peace Garden', 'city': 'Fargo', 'state': 'North Dakota', 'address': '200 Broadway N', 'zip': '58102', 'lat': 46.8772, 'long': -96.7881, 'phone': '(701) 555-0577'},
            {'dealer_id': 50, 'full_name': 'Equality State Motors', 'short_name': 'Equality Motors', 'city': 'Cheyenne', 'state': 'Wyoming', 'address': '200 W 17th St', 'zip': '82001', 'lat': 41.1342, 'long': -104.8181, 'phone': '(307) 555-0588'}
        ]

        for ddata in dealers_data:
            Dealer.objects.update_or_create(
                dealer_id=ddata['dealer_id'],
                defaults=ddata
            )

        self.stdout.write(self.style.SUCCESS(f'{len(dealers_data)} Dealers populated.'))

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
                'dealer_id': 1,
                'name': 'John Doe',
                'review': 'Outstanding customer service and smooth car delivery!',
                'purchase': True,
                'purchase_date': '2024-03-01',
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
