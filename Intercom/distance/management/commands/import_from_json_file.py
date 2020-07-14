
import os
import json
from distance.models import Customer
from django.core.management.base import BaseCommand
from datetime import datetime
from Intercom.settings import BASE_DIR


class Command(BaseCommand):
    def import_customer_from_file(self):
        data_folder = os.path.join(BASE_DIR, 'distance', 'resources/json_file')
        for data_file in os.listdir(data_folder):
            with open(os.path.join(data_folder, data_file), encoding='utf-8') as data_file:
                data = json.loads(data_file.read())
                for data1 in data:
                    name = data1.get('name', None)
                    user_id = data1.get('user_id', None)
                    latitude = data1.get('latitude', None)
                    longitude = data1.get('longitude', None)


                    try:
                        customer, created = Customer.objects.get_or_create(
                            name=name,
                            user_id = user_id,
                            latitude = latitude,
                            longitude = longitude
                        )
                        if created:
                            customer.save()
                            display_format = "\ncustomer, {}, has been saved."
                            print(display_format.format(customer))
                    except Exception as ex:
                        print(str(ex))
                        msg = "\n\nSomething went wrong saving this movie: {}\n{}".format(name, str(ex))
                        print(msg)


    def handle(self, *args, **options):
        self.import_customer_from_file()
