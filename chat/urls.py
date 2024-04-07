from django.urls import path

from chat import views


app_name = 'chat'

urlpatterns = [
    path('', views.RolePlayingRoomListView.as_view(), name='role_playing_room_list'),
    path('new/', views.RolePlayingRoomCreateView.as_view(), name='role_playing_room_new'),
    path('<int:pk>/', views.RolePlayingRoomDetailView.as_view(), name='role_playing_room_detail'),
    path('<int:pk>/edit/', views.RolePlayingRoomUpdateView.as_view(), name='role_playing_room_edit'),
    path('<int:pk>/delete/', views.RolePlayingRoomDeleteView.as_view(), name='role_playing_room_delete'),
]