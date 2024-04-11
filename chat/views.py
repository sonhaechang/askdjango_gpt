from typing import Any

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
)

from chat.forms import RolePlayingRoomForm
from chat.models import RolePlayingRoom

from gtts import gTTS


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
class RolePlayingRoomDetailView(DetailView):
    model = RolePlayingRoom
    template_name = 'chat/container/role_playing_room_detail.html'
    context_object_name = 'role_playing_room'

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
    

@method_decorator(staff_member_required, name='dispatch')
class RolePlayingRoomDeleteView(DeleteView):
    model = RolePlayingRoom
    success_url = reverse_lazy('chat:role_playing_room_list')
    template_name = 'chat/container/role_playing_room_confirm_delete.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)

        return qs
    
    def form_valid(self, form: Any) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, _('채팅방을 삭제했습니다.'))

        return response
    
    
@staff_member_required
def make_voice(request) -> HttpResponse:
    lang = request.GET.get('lang', 'en')
    message = request.GET.get('message')

    response = HttpResponse()
    gTTS(message, lang=lang).write_to_fp(response)
    response['Content-Type'] = 'audio/mpeg'

    return response