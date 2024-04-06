from typing import Any
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from chat.forms import RolePlayingRoomForm
from chat.models import RolePlayingRoom


# Create your views here.
@method_decorator(staff_member_required, name='dispatch')
class RolePlayingRoomListView(ListView):
    model = RolePlayingRoom
    template_name = 'chat/container/role_playing_room_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)

        return qs


@method_decorator(staff_member_required, name='dispatch')
class RolePlayingRoomCreateView(CreateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm
    template_name = 'chat/container/create_role_playing_room.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        role_playing_room = form.save(commit=False)
        role_playing_room.user = self.request.user

        return super().form_valid(form)
    

@method_decorator(staff_member_required, name='dispatch')
class RolePlayingRoomUpdateView(UpdateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm
    template_name = 'chat/container/update_role_playing_room.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)

        return qs