from django.contrib import admin
from .models import User, Venue, Category, Event_Data  # Ensure the model names match exactly

# Register your models here.
admin.site.register(User)
admin.site.register(Venue)
admin.site.register(Category)
admin.site.register(Event_Data)