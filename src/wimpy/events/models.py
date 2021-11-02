from datetime import datetime
from typing import Dict

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _

from wimpy.constants import DEFAULT_DATETIME_FORMAT
from wimpy.events.constants import get_default_event_data_schema

__all__ = ['EventCategory', 'EventType', 'EventSchema', 'Event']


class EventCategory(models.Model):

    name = models.CharField(
        verbose_name=_('Category name'),
        help_text=_('Name of category used to generate a unique slug'),
        max_length=64,
        null=False,
        blank=False,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_('Category description'),
        help_text=_('Brief description about category'),
        max_length=256,
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        verbose_name=_('Category slug'),
        help_text=_('Identifier used to interact with API'),
        max_length=64,
        null=False,
        blank=False,
        db_index=True,
        editable=False,
    )

    def __str__(self):
        return self.slug or ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(EventCategory, self).save(*args, **kwargs)


class EventType(models.Model):

    name = models.CharField(
        verbose_name=_('Type name'),
        help_text=_('Name of type used to generate a unique slug'),
        max_length=64,
        null=False,
        blank=False,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_('Type description'),
        help_text=_('Brief description about type'),
        max_length=256,
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        verbose_name=_('Type slug'),
        help_text=_('Identifier used to interact with API'),
        max_length=64,
        null=False,
        blank=False,
        db_index=True,
        editable=False,
    )

    def __str__(self):
        return self.slug or ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(EventType, self).save(*args, **kwargs)


class EventSchema(models.Model):

    category = models.ForeignKey('EventCategory', on_delete=models.CASCADE)
    type = models.ForeignKey('EventType', on_delete=models.CASCADE)

    data_schema = models.JSONField(
        verbose_name=_('Event data schema'),
        help_text=_('Custom json schema to validate event data'),
        null=True,
        blank=True,
        default=get_default_event_data_schema,
    )

    class Meta:
        unique_together = ('category', 'type',)

    def __str__(self):
        return f'{self.category} - {self.type}'


class Event(models.Model):

    session_id = models.UUIDField(db_index=True)
    category = models.ForeignKey('EventCategory', on_delete=models.CASCADE)
    name = models.ForeignKey('EventType', on_delete=models.CASCADE)
    data = models.JSONField(
        verbose_name=_('Event data'),
        help_text=_('Event data sent from client'),
        null=False,
        blank=False,
    )
    timestamp = models.DateTimeField(
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ('timestamp',)

    def to_json(self) -> Dict:
        return {
            'session_id': str(self.session_id),
            'category': self.category.slug,
            'name': self.name.slug,
            'data': self.data,
            'timestamp': datetime.strftime(
                self.timestamp,
                DEFAULT_DATETIME_FORMAT
            ),
        }
