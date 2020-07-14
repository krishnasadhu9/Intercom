from django.shortcuts import render

import math as np
import requests
import json
from distance.models import Customer
from django.core.management.base import BaseCommand
from datetime import datetime
from operator import itemgetter

IMPORT_URL = 'https://s3.amazonaws.com/intercom-take-home-test/customers.txt'

def import_customer(data):
    name = data.get('name', None)
    user_id = data.get('user_id', None)
    latitude = data.get('latitude', None)
    longitude = data.get('longitude', None)
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
        msg = "\n\nSomething went wrong saving this customer: {}\n{}".format(title, str(ex))
        print(msg)

def customer(request):
    if request.method == "POST":
        headers = {'Content-Type': 'application/json'}
        response = requests.get(
        url=IMPORT_URL,
        headers=headers,
        )
        response.raise_for_status()
        data = response.json()
        print(data);
        for data_object in data:
            import_customer(data_object)


def viewall(request):
    if request.method == "POST":
        r = 6371
        lon1 = -6.257664
        lat1 = 53.339428
        intercom1 = np.radians(lat1)

        customer_list = []

        customers = Customer.objects.all()

        for customer in customers:
            final_customer ={}
            lat2 = float(customer.latitude)
            lon2 = float(customer.longitude)
            intercom2 = np.radians(lat2)
            intercom_phi = np.radians(lat2 - lat1)
            intercom_lambda = np.radians(lon2 - lon1)
            a = np.sin(intercom_phi / 2)**2 + np.cos(intercom1) * np.cos(intercom2) * np.sin(intercom_lambda / 2)**2
            res = r * (2 * np.atan2(np.sqrt(a), np.sqrt(1 - a)))
            res = round(res,2)
            final_customer["user_id"] = customer.user_id
            final_customer["name"] = customer.name
            final_customer["latitude"] = customer.latitude
            final_customer["longitude"] = customer.longitude
            final_customer["Distance"] = res
            customer_list.append(final_customer)
            customer_list = sorted(customer_list, key=itemgetter('user_id')) 
        return render(request,'allcustomers.html', { "customer" : customer_list} )
    return render(request,'home.html')


def intercom_view(request):
    if request.method == "POST":
        r = 6371
        lon1 = -6.257664
        lat1 = 53.339428
        intercom1 = np.radians(lat1)

        customer_list = []

        customers = Customer.objects.all()


        for customer in customers:
            final_customer ={}
            lat2 = float(customer.latitude)
            lon2 = float(customer.longitude)
            intercom2 = np.radians(lat2)
            intercom_phi = np.radians(lat2 - lat1)
            intercom_lambda = np.radians(lon2 - lon1)
            a = np.sin(intercom_phi / 2)**2 + np.cos(intercom1) * np.cos(intercom2) * np.sin(intercom_lambda / 2)**2
            res = r * (2 * np.atan2(np.sqrt(a), np.sqrt(1 - a)))
            res = round(res,2)
            if res <= 100:
                final_customer["user_id"] = customer.user_id
                final_customer["name"] = customer.name
                final_customer["latitude"] = customer.latitude
                final_customer["longitude"] = customer.longitude
                final_customer["Distance"] = res
                customer_list.append(final_customer)
                customer_list = sorted(customer_list, key=itemgetter('user_id'))
        return render(request,'100kmintercom.html', { "customer" : customer_list} )
    return render(request,'home.html')
