from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import AuditLogEntry

@registry.register_document
class AuditLogDocument(Document):
    
    class Index:
        name = 'auditlog'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }

    class Django:
         model = AuditLogEntry
         fields = [
             'is_sent',
             'message',
             'created_at'
         ]