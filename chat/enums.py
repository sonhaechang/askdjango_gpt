from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class LanguageEnum(TextChoices):
    ''' 상황극 채팅방 언어 구분 클래스  '''

    ENGLISH = 'en-US', _('English')
    JAPANESE = 'ja-JP', _('Japanese')
    CHINESE = 'zh-CN', _('Chinese')
    SPANISH = 'es-ES', _('Spanish')
    FRENCH = 'fr-FR', _('French')
    GERMAN = 'de-DE', _('German')
    RUSSIAN = 'ru-RU', _('Russian')


class LevelEnum(TextChoices):
    ''' 상황극 채팅방 레벨 구분 클래스  '''

    BEGINNER = 1, _('초급')
    ADVANCED = 2, _('고급')