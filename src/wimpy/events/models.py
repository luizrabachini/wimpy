from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _

from wimpy.events.constants import get_default_event_data_schema

__all__ = ['EventCategory', 'EventType']


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
        unique=True,
        editable=False,
    )

    def __str__(self):
        return self.slug or ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(EventCategory, self).save(*args, **kwargs)


class EventType(models.Model):

    category = models.ForeignKey('EventCategory', on_delete=models.CASCADE)

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
        unique=True,
        editable=False,
    )

    data_schema = models.JSONField(
        verbose_name=_('Event data schema'),
        help_text=_('Custom json schema to validate event data'),
        null=True,
        blank=True,
        default=get_default_event_data_schema,
    )

    def __str__(self):
        return self.slug or ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(EventType, self).save(*args, **kwargs)
