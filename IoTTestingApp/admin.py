# IoTTestingApp/admin.py
from django.contrib import admin
from .models import IoTGeneratedData

@admin.register(IoTGeneratedData)
class IoTGeneratedDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'second', 'src', 'dst', 'packetcount', 'label', 'created_at')
    list_filter = ('label', 'created_at')
    search_fields = ('src', 'dst')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Time Information', {
            'fields': ('second', 'created_at')
        }),
        ('Network Information', {
            'fields': ('src', 'dst', 'packetcount')
        }),
        ('Ratios', {
            'fields': ('src_ratio', 'dst_ratio', 'src_duration_ratio', 'dst_duration_ratio',
                      'src_packet_ratio', 'dst_packet_ratio')
        }),
        ('Packet Information', {
            'fields': ('TotalPacketDuration', 'TotalPacketLenght')
        }),
        ('Message Counts', {
            'fields': ('DioCount', 'DisCount', 'DaoCount', 'OtherMsg')
        }),
        ('Classification', {
            'fields': ('label',)
        })
    )