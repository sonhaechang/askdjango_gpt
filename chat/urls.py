from django.urls import path

from chat import views


app_name = 'chat'

urlpatterns = [
    path('new/', views.RolePlayingRoomCreateView.as_view(), name='role_playing_room_new'),
]