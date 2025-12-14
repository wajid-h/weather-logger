from django.contrib import admin
from . models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "temprature_celsius",
        "humidity_percent",
        "timestamp",
    )

    sortable_by = ("temprature", "humidity", "timestamp")
    readonly_fields = ("timestamp",)

    def temprature_celsius(self, obj):
        return f"{obj.temprature} °C"

    temprature_celsius.short_description = "Temperature"
    temprature_celsius.admin_order_field = "temprature"

    def humidity_percent(self, obj):
        return f"{obj.humidity} %"

    humidity_percent.short_description = "Humidity"
    humidity_percent.admin_order_field = "humidity"    