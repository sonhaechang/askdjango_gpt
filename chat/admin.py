from typing import Any
from django.contrib import admin

from chat.forms import AdminRolePlayingRoomForm
from chat.models import RolePlayingRoom


# Register your models here.
@admin.register(RolePlayingRoom)
class RolePlayingRoomAdmin(admin.ModelAdmin):
    form = AdminRolePlayingRoomForm

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        return super().save_model(request, obj, form, change)