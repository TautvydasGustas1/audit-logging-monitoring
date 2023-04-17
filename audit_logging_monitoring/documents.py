from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import AuditLogEntry


# current_time = get_time()
@registry.register_document
class AuditLogDocument(Document):
    
    class Index:
        name = 'audit-auditlog-django-test-prod'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }



    class Django:
         model = AuditLogEntry
         fields = {
             'message',
             'timestamp'
         }





    