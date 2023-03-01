from django.utils import timezone


def get_year():
    return timezone.now().year
