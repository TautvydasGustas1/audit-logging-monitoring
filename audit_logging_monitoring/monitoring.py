
import datetime
from time import strftime
from django.http import HttpResponse
from django.http import JsonResponse

from audit_logging_monitoring.models import AuditLogEntry
from django.db.models.signals import post_save
from audit_logging_monitoring.documents import AuditLogDocument



def main(request):
    return JsonResponse({'response':"ElasticCloud audit log service OK"})

def monitor(request):
    try:
        auditLog = AuditLogEntry(
        is_sent=True,
        message="Works",
        )
        post_save.send(AuditLogEntry, instance=auditLog, created=True)
    except Exception as err:
        print("Exception occured when saving new entry to elasticsearch:", err)
        return JsonResponse(status=500, data={'response':"Error saving new entry to ElasticSearch"})
    

    date_now = datetime.datetime.now()
    date_yesterday = datetime.datetime.now() - datetime.timedelta(1)
    found = False

    try:
        s = AuditLogDocument.search().query('range', **{'created_at': {'gte': date_yesterday, 'lte': date_now}}).sort("-created_at")
    except Exception as err: 
        print("Error getting entry from elasticsearch:", err)
        return JsonResponse(status=500, data={'response':"Error getting entry from ElasticSearch"})

    for hit in s:

        if not found:
            last_entry = hit

        found = True

        print(
            "Category name : {}, Created at - {}".format(hit.message, hit.created_at)
        )

    if found == False:
        print("Empty")
        return JsonResponse(status=500, data={'response':"No entry has been found"})


    return JsonResponse({'response':"ElasticCloud audit log service OK, latest entry - " + strftime(str(last_entry.created_at))})
