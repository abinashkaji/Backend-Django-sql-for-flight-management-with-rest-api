from django.db import models
# Create your models here.
class Airport(models.Model):
    city=models.CharField(max_length=20)
    code=models.CharField(max_length=3)

    def __str__(self) -> str:
        return f"{self.city} '{self.code} "

class Flight(models.Model):
    origin=models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="Departure")
    destination=models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="arrival")
    duration=models.IntegerField()

    def __str__(self) -> str:
        return f" {self.origin} to {self.destination}, Time: {self.duration} "

class Passenger(models.Model):
    first=models.CharField(max_length=20)
    last=models.CharField(max_length=20)
    flights=models.ManyToManyField(Flight,blank=True, related_name="passengers")

    def __str__(self) -> str:
        return f"{self.first} {self.last} "