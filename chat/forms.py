from django import forms
from django.utils.translation import gettext_lazy as _

from chat.models import RolePlayingRoom
from chat.translators import google_translate


class BaseRolePlayingRoomForm(forms.ModelForm):
    class Meta:
        model = RolePlayingRoom
        fields = '__all__'

    def clean(self):
        translates = {
            'situation': self.cleaned_data.get('situation'),
            'situation_en': self.cleaned_data.get('situation_en'),
            'my_role': self.cleaned_data.get('my_role'),
            'my_role_en': self.cleaned_data.get('my_role_en'),
            'gpt_role': self.cleaned_data.get('gpt_role'),
            'gpt_role_en': self.cleaned_data.get('gpt_role_en'),
        }

        for idx, field in enumerate(translates.keys()):
            if idx % 2 == 0 and translates[field] and not translates[f'{field}_en']:
                self.cleaned_data[f'{field}_en'] = self._translate(translates[field])

    @staticmethod
    def _translate(origin_text: str) -> str:
        translated = google_translate(origin_text, 'auto', 'en')

        if not translated:
            raise forms.ValidationError(_('구글 번역에 실패했습니다.'))
        
        return translated


class AdminRolePlayingRoomForm(BaseRolePlayingRoomForm):
    pass

class RolePlayingRoomForm(BaseRolePlayingRoomForm):
    class Meta:
        model = RolePlayingRoom
        fields = [
            'language',
            'level',
            'situation',
            'situation_en',
            'my_role',
            'my_role_en',
            'gpt_role',
            'gpt_role_en',
        ]