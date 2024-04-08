from typing import List, Literal, TypedDict

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from chat.enums import LanguageEnum, LevelEnum


# Create your models here.
class GptMessage(TypedDict):
    role: Literal['system', 'user', 'assistant']
    content: str


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

    def __str__(self) -> str:
        return self.situation

    def get_absolute_url(self) -> str:
        return reverse('chat:role_playing_room_detail', args=[self.pk])
    
    def get_initial_messages(self) -> List[GptMessage]:
        gpt_name = 'RolePalyingBot'
        language = self.get_language_display()
        situation_en = self.situation_en
        my_role_en = self.my_role_en
        gpt_role_en = self.gpt_role_en

        if self.level == LevelEnum.BEGINNER:
            level_string = f'a beginner in {language}'
            level_word = 'simple'
        elif self.level == LevelEnum.ADVANCED:
            level_string = f'a beginner in {language}'
            level_word = 'advanced'
        else:
            raise ValueError(f'Invalid level : {self.level}')
        
        system_message = (
            f"You are helpful assistant supporting people learning {language}. "
            f"Your name is {gpt_name}. "
            f"Please assume that the user you are assisting is {level_string}. "
            f"And please write only the sentence without the character role."
        )

        user_message = (
            f"Let's have a conversation in {language}. "
            f"Please answer in {language} only "
            f"without providing a translation. "
            f"And please don't write down the pronunciation either. "
            f"Let us assume that the situation in '{situation_en}'. "
            f"I am {my_role_en}. The character I want you to act as is {gpt_role_en}. "
            f"Please make sure that I'm {level_string}, so please use {level_word} words "
            f"as much as possible. Now, start a conversation with the first sentence!"
        )

        return [
            GptMessage(role='system', content=system_message),
            GptMessage(role='user', content=user_message),
        ]
    
    def get_recommend_message(self) -> str:
        level = self.level

        if level == LevelEnum.BEGINNER:
            level_word = 'smiple'
        elif level == LevelEnum.ADVANCED:
            level_word = 'advanced'
        else:
            raise ValueError(f'Invalid level : {level}')
        
        return (
            f'Can you please provide me an {level_word} example '
            f'of how to respond to the last sentence '
            f'in this situation, without providing a translation '
            f'and any introductory phrases or sentences.'
        )