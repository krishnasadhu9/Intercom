from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=30)
    user_id = models.IntegerField(unique = True)
    latitude = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True)

    def __str__(self):
        return self.name +  "\n user_id:" + str(self.user_id) + " \nLatitude: " + str(self.latitude) + "\nLongitude " + str(self.longitude) 
