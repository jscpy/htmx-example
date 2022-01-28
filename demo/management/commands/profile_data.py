from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from demo.models import Profile

class Command(BaseCommand):
    help = 'Create random data for Profile model'
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--total', '-t', type=int, help='Indicates the number of Profiles to be create')
        parser.add_argument('--job', '-j', type=str, help='Job description')
        parser.add_argument('--company', '-c' ,type=str, help='Company description')
        parser.add_argument('--delete', '-d', type=bool, default=False, help='Delete all previous data')
        parser.add_argument('--random', '-r', type=bool, default=False, help='Random data')

    def handle(self, *args: Any, **kwargs: Any) -> Optional[str]:
        fake = Faker()
        total = kwargs.get('total', 1)
        job = kwargs.get('job', '')
        company = kwargs.get('company', '')
        delete_all = kwargs.get('delete')
        is_random = kwargs.get('random')
        
        if delete_all:
            rows = Profile.objects.all()
            rows.delete()
        
        if is_random:
            for i in range(total):
                Profile.objects.create(
                    first_name=fake.first_name(), last_name=fake.last_name(),
                    address=fake.address(), phonenumber=fake.phone_number(),
                    email=fake.email(), job=fake.job(), company=fake.company()
                )
        else:
            for i in range(total):
                Profile.objects.create(
                    first_name=fake.first_name(), last_name=fake.last_name(),
                    address=fake.address(), phonenumber=fake.phone_number(),
                    email=fake.email(), job=job, company=company
                )