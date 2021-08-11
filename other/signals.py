from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from other.models import Project


@receiver(pre_save, sender=Project)
def check_regions_limit(sender, instance, **kwargs):
    if instance.main_categories.count() > 2:
        raise ValidationError("Вы не можете выбрать больше двух категорий")
