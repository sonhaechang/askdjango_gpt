from django.contrib.admin.views.decorators import staff_member_required
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from chat.forms import RolePlayingRoomForm
from chat.models import RolePlayingRoom


# Create your views here.
@method_decorator(staff_member_required, name='dispatch')
class RolePlayingRoomCreateView(CreateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm
    template_name = 'chat/container/create_role_playing_room.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        role_playing_room = form.save(commit=False)
        role_playing_room.user = self.request.user
        return super().form_valid(form)