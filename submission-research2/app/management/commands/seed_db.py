from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from app.models import User, Company, UserProfile
import json
import os

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database seed...')
        
        try:
            # Load fixture data
            fixture_path = os.path.join('app', 'fixtures', 'initial_data.json')
            with open(fixture_path, 'r') as file:
                data = json.load(file)

            # Seed Users
            self.stdout.write('Seeding users...')
            users_map = {}  # To store user instances
            for user_data in data['users']:
                fields = user_data['fields']
                # Hash the password properly
                fields['password'] = make_password('@345678')
                user, created = User.objects.get_or_create(
                    email=fields['email'],
                    defaults=fields
                )
                users_map[user_data['pk']] = user

            # Seed Companies
            self.stdout.write('Seeding companies...')
            companies_map = {}  # To store company instances
            for company_data in data['companies']:
                fields = company_data['fields']
                company, created = Company.objects.get_or_create(
                    name=fields['name'],
                    defaults=fields
                )
                companies_map[company_data['pk']] = company

            # Seed UserProfiles
            self.stdout.write('Seeding user profiles...')
            for profile_data in data['profiles']:
                fields = profile_data['fields'].copy()  # Create a copy to modify
                # Replace IDs with actual instances
                fields['user'] = users_map[fields['user']]
                fields['company'] = companies_map[fields['company']]
                
                UserProfile.objects.get_or_create(
                    user=fields['user'],
                    company=fields['company'],
                    defaults=fields
                )

            self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding database: {str(e)}'))
            raise e 