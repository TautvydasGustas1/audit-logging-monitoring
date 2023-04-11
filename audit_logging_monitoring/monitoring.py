
import datetime
from time import strftime
from django.http import HttpResponse
from django.http import JsonResponse

from audit_logging_monitoring.models import AuditLogEntry
from django.db.models.signals import post_save
from django.utils import timezone
from audit_logging_monitoring.documents import AuditLogDocument



def main(request):
    return JsonResponse({'response':"ElasticCloud audit log service OK"})

def create(request):
    try:
        auditLog = AuditLogEntry(
        is_sent=True,
        message="Works",
        )
        post_save.send(AuditLogEntry, instance=auditLog, created=True)
    except Exception as err:
        print("Exception occured when saving new entry to elasticsearch:", err)
        return JsonResponse(status=500, data={'response':"Error saving new entry to ElasticSearch"})
        
    return JsonResponse({'response':"Created new entry to ElasticSearch"})

def search(request):

    date_now = datetime.datetime.now()
    date_yesterday = datetime.datetime.now() - datetime.timedelta(1)
    found = False

    s = AuditLogDocument.search().query('range', **{'created_at': {'gte': date_yesterday, 'lte': date_now}}).sort("-created_at")
    

    for hit in s:

        if not found:
            last_entry = hit

        found = True

        print(
            "Category name : {}, Created at - {}".format(hit.message, hit.created_at)
        )

        

    if found == False:
        print("Empty")

    return JsonResponse({'response':"Found latest entry - " + strftime(str(last_entry.created_at))})
