import json
from django.core.management.base import BaseCommand
from accounts.models import Student

class Command(BaseCommand):
    help = 'import external JSON file into Django database'

    def handle(self, *args, **kwargs):

        try:
            
            with open('/home/abhinav/Desktop/hello_django/school_managment/sudents_data.json','r',encoding='utf8') as file:
                data = json.load(file)
                print(data)

                for item in data:
                    Student.objects.create(
                    first_name=item['first_name'],
                    last_name=item['last_name'],
                    date_of_birth=item['date_of_birth'],
                    gender=item['gender'],
                    email=item['email'],
                    phone_number=item['phone_number'],
                    address=item['address'],
                    date_of_enrollment=item['date_of_enrollment'],
                    current_class=item['current_class'],
                    section=item['section'],
                    total_fees=item['total_fees'],
                    fees_paid=item['fees_paid'],
                    outstanding_fees=item['outstanding_fees']
                )
            self.stdout.write(self.style.SUCCESS('Done'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))