from django.db import models

class InteractionLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)
    device_ip = models.CharField(max_length=50, blank=True, null=True)
    result = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.action} - {self.result}"