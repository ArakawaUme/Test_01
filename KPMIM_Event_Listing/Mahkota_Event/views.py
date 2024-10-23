from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Event_Data, Venue, Category
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db.models import Q 
from django.contrib.auth import logout

def login(request):
    if request.method == 'POST':
        c_email = request.POST.get('email')
        c_password = request.POST.get('password')

        try:
            user = User.objects.get(email=c_email)
            if user.password == c_password:
                request.session['user_id'] = user.user_id
                return redirect('main_page')
            else:
                messages.error(request, 'Invalid password. Please try again.')
                return render(request, 'login.html')

        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'login.html')

    return render(request, "login.html")

def create_acc(request):
    if request.method == 'POST':
        user_id = request.POST["user_id"]
        name = request.POST["name"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]
        password = request.POST["password"]

        data = User(user_id=user_id, name=name, phone_number=phone_number, email=email, password=password)
        data.save()

        messages.success(request, "Register New Account Complete")
        return redirect('login')

    User_Insert = User.objects.all().values()
    context = {
        'User': User_Insert,
    }

    return render(request, "create_acc.html", context)

def main_page(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You need to be logged in to view your events.")
        return redirect('login')

    try:
        organizer = User.objects.get(user_id=user_id)
        organized_events = Event_Data.objects.filter(organized_id=organizer)

    except User.DoesNotExist:
        messages.error(request, "Organizer not found.")
        return redirect('login')

    context = {
        'organized_events': organized_events,
    }

    return render(request, "main_page.html", context)

def registration(request):
    venues = Venue.objects.all()
    categories = Category.objects.all()

    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You need to be logged in to create an event.")
        return redirect('login')

    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event_name = request.POST.get('event_name')
        start_event_date = request.POST.get('start_date')
        start_event_time = request.POST.get('start_time')
        end_event_date = request.POST.get('end_date')
        end_event_time = request.POST.get('end_time')
        venue_id = request.POST.get('venue_id')
        category_id = request.POST.get('category_id')

        if not all([event_id, event_name, start_event_date, start_event_time, end_event_date, end_event_time, venue_id, category_id]):
            messages.error(request, "Please fill in all the fields.")
            return render(request, 'registration.html', {'venues': venues, 'categories': categories})

        try:
            organized_id = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            messages.error(request, "Organizer not found.")
            return redirect('registration')

        try:
            venue = Venue.objects.get(venue_id=venue_id)
        except ObjectDoesNotExist:
            messages.error(request, "Selected venue does not exist.")
            return redirect('registration')

        try:
            category = Category.objects.get(category_id=category_id)
        except ObjectDoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('registration')

        new_event = Event_Data(
            event_id=event_id,
            event_name=event_name,
            start_event_date=start_event_date,
            start_event_time=start_event_time,
            end_event_date=end_event_date,
            end_event_time=end_event_time,
            venue_id=venue,
            category_id=category,
            organized_id=organized_id
        )
        new_event.save()

        messages.success(request, 'Event successfully registered.')
        return redirect('event_list')

    context = {
        'venues': venues,
        'categories': categories,
    }

    return render(request, 'registration.html', context)

def event_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        events = Event_Data.objects.filter(
            Q(event_name__icontains=search_query) |
            Q(organized_id__name__icontains=search_query) |
            Q(category_id__category_name__icontains=search_query) |
            Q(venue_id__venue_name__icontains=search_query) |
            Q(event_id__icontains=search_query)
        )
    else:
        events = Event_Data.objects.all()

    venue_ids = events.values_list('venue_id', flat=True).distinct()
    category_ids = events.values_list('category_id', flat=True).distinct()

    venues = Venue.objects.filter(venue_id__in=venue_ids)
    categories = Category.objects.filter(category_id__in=category_ids)

    context = {
        'events': events,
        'venues': venues,
        'categories': categories,
    }

    return render(request, "event_list.html", context)

def delete_event(request, event_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You need to be logged in to delete an event.")
        return redirect('login')

    event = get_object_or_404(Event_Data, event_id=event_id)

    if event.organized_id.user_id != user_id:
        messages.error(request, "You are not authorized to delete this event.")
        return redirect('event_list')

    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('event_list')

def update_event(request, event_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You need to be logged in to update an event.")
        return redirect('login')

    event = get_object_or_404(Event_Data, event_id=event_id)

    if event.organized_id.user_id != user_id:
        messages.error(request, "You are not authorized to update this event.")
        return redirect('event_list')

    venues = Venue.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        event_name = request.POST.get('event_name')
        start_event_date = request.POST.get('start_date')
        start_event_time = request.POST.get('start_time')
        end_event_date = request.POST.get('end_date')
        end_event_time = request.POST.get('end_time')
        venue_id = request.POST.get('venue_id')
        category_id = request.POST.get('category_id')

        event.event_name = event_name
        event.start_event_date = start_event_date
        event.start_event_time = start_event_time
        event.end_event_date = end_event_date
        event.end_event_time = end_event_time
        event.venue_id = Venue.objects.get(venue_id=venue_id)
        event.category_id = Category.objects.get(category_id=category_id)

        event.save()
        messages.success(request, "Event updated successfully.")
        return redirect('event_list')

    context = {
        'event': event,
        'venues': venues,
        'categories': categories,
    }
    return render(request, 'update_event.html', context)

def edit_profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('login')

    user = get_object_or_404(User, user_id=user_id)

    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        user.name = request.POST.get('name')
        user.phone_number = request.POST.get('phone_number')
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('main_page')

    context = {
        'user': user,
    }

    return render(request, 'edit_profile.html', context)

def delete_user(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "You need to be logged in to delete your account.")
        return redirect('login')

    user = get_object_or_404(User, user_id=user_id)

    user.delete()
    
    logout(request)
    request.session.flush()

    messages.success(request, "Your account has been deleted successfully.")
    return redirect('main_page')
