from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from chat.enums import LanguageEnum, LevelEnum


# Create your models here.
class RolePlayingRoom(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_user_set',
        verbose_name=_('사용자')
    )

    language = models.CharField(
        max_length=10,
        choices=LanguageEnum.choices,
        default=LanguageEnum.ENGLISH,
        verbose_name=_('대화 언어')
    )

    level = models.SmallIntegerField(
        choices=LevelEnum.choices,
        default=LevelEnum.BEGINNER,
        verbose_name=_('레벨'),
    )

    situation = models.CharField(
        max_length=100,
        verbose_name=_('상황')
    )

    situation_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('상황 (영문)'),
        help_text=_(
            'GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, ' +
            'situation 필드를 번역하여 자동 반영됩니다.'
        )
    )

    my_role = models.CharField(
        max_length=100,
        verbose_name=_('내 역할')
    )

    my_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('내 역할 (영문)'),
        help_text=_(
            'GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, ' +
            'my_role 필드를 번역하여 자동 반영됩니다.'
        )
    )

    gpt_role = models.CharField(
        max_length=100,
        verbose_name=_('GPT 역할')
    )

    gpt_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('GPT 역할 (영문)'),
        help_text=_(
            'GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, ' +
            'gpt_role 필드를 번역하여 자동 반영됩니다.'
        )
    )

    class Meta:
        db_table = 'role_playing_room_tb'
        verbose_name = _('상항극 채팅방')
        verbose_name_plural = _('상항극 채팅방')
        ordering = ('-id',)