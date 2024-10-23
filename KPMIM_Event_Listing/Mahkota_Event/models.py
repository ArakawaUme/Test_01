from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)    
    
    def __str__(self):
        return self.name
     
class Category(models.Model):
    category_id = models.CharField(max_length=20, primary_key=True)
    category_name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=50)
    category_description = models.TextField()

class Venue(models.Model):
    venue_id = models.CharField(max_length=20, primary_key=True)
    venue_name = models.CharField(max_length=100)
    location = models.CharField(max_length=500)

class Event_Data(models.Model):
    event_id = models.CharField(max_length=20, primary_key=True)
    event_name = models.CharField(max_length=100)
    start_event_date = models.DateField()
    start_event_time = models.TimeField()
    end_event_date = models.DateField()
    end_event_time = models.TimeField()
    organized_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
    