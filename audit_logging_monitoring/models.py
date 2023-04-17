from django.utils import timezone
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class AuditLogEntry(models.Model):
    message = models.TextField(verbose_name=_("message"))
    timestamp = models.DateTimeField(verbose_name=_("@timestamp"))


    class Meta:
        app_label = 'auditlog'


def _safe_get(value: dict, *keys: str) -> str:
    """Look up a nested key in the given dict, or return "UNKNOWN" on KeyError."""
    for key in keys:
        try:
            value = value[key]
        except KeyError:
            return "UNKNOWN"
    return str(value) or "UNKNOWN"

