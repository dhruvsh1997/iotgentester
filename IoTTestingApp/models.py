# IoTTestingApp/models.py
from django.db import models

class IoTGeneratedData(models.Model):
    second = models.FloatField()
    src = models.IntegerField()
    dst = models.IntegerField()
    packetcount = models.IntegerField()
    src_ratio = models.FloatField()
    dst_ratio = models.FloatField()
    src_duration_ratio = models.FloatField()
    dst_duration_ratio = models.FloatField()
    TotalPacketDuration = models.FloatField()
    TotalPacketLenght = models.IntegerField()
    src_packet_ratio = models.FloatField()
    dst_packet_ratio = models.FloatField()
    DioCount = models.IntegerField()
    DisCount = models.IntegerField()
    DaoCount = models.IntegerField()
    OtherMsg = models.IntegerField()
    label = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"IoT Data {self.id} - {self.created_at}"