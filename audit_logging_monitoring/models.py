from django.utils import timezone
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class AuditLogEntry(models.Model):
    is_sent = models.BooleanField(default=False, verbose_name=_("is sent"))
    message = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("created at"))

    class Meta:
        app_label = 'auditlog'

    # def pre_save(self, model_instance, add):
    #     return timezone.now()

    # #usage
    # created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return ", ".join(
            [
                "Is sent: " + str(self.is_sent),
                "Message: " + str(self.message),
                "Created at: " + str(self.created_at)
            ]
        )