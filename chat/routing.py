from django.urls import path

from chat import consumers


websocket_urlpstterns = [
    path('ws/chat/<int:room_pk>/', consumers.RolePlayingRoomConsumer.as_asgi()),
]