from django.urls import path

from chat import views


app_name = 'chat'

urlpatterns = [
    path('', views.RolePlayingRoomListView.as_view(), name='role_playing_room_list'),
    path('new/', views.RolePlayingRoomCreateView.as_view(), name='role_playing_room_new'),
    path('<int:pk>/edit/', views.RolePlayingRoomUpdateView.as_view(), name='role_playing_room_edit'),
]