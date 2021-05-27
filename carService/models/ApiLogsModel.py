from django.db import models
from django.db.models import Model


class APILogsModel(Model):
    id = models.BigAutoField(primary_key=True)
    api = models.CharField(max_length=512, help_text='API URL')
    headers = models.TextField()
    body = models.TextField()
    method = models.CharField(max_length=10, db_index=True)
    client_ip_address = models.CharField(max_length=50)
    response = models.TextField()
    status_code = models.PositiveSmallIntegerField(help_text='Response status code', db_index=True)
    execution_time = models.DecimalField(decimal_places=5, max_digits=8,
                                         help_text='Server execution time (Not complete response time.)')
    added_on = models.DateTimeField()
