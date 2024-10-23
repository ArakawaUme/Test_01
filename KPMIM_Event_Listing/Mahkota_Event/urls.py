from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("create_acc/", views.create_acc, name="create_acc"),
    path("homepage/", views.main_page, name="main_page"),
    path("register/", views.registration, name="registration"),
    # path("database/", views.database, name="database"),
    path("event_list/", views.event_list, name="event_list"),
    path('event/delete/<str:event_id>/', views.delete_event, name='delete_event'),
    path('event/update/<str:event_id>/', views.update_event, name='update_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/update/', views.update_event, name='update_event'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_user/', views.delete_user, name='delete_user'),
]