from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from .models import LogEntry
from django.utils import timezone
from datetime import timedelta

logs_since_boot = 0
sequential_zero_push = 0

@csrf_exempt
def index(request):
    global logs_since_boot
    global sequential_zero_push
    
    if request.method == "POST":
        if logs_since_boot < 3:
            logs_since_boot += 1
            return HttpResponse("Ignoring first 3 pushes to keep data sterile")
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)
        
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        
        if temperature is None or humidity is None:
            return HttpResponse("No data, ignored.")
        
        if temperature == 0 and humidity == 0:
            sequential_zero_push += 1
            if sequential_zero_push <= 3:
                return HttpResponse("'0' values received, likely failed read — waiting")
        else:
            sequential_zero_push = 0
        
        LogEntry.objects.create(
            temprature=temperature,
            humidity=humidity
        )
        return HttpResponse("Data logged successfully")
    
    # --- GET request: render dashboard ---
    recent_entries = LogEntry.objects.order_by('-timestamp')[:30]
    latest_entry = LogEntry.objects.order_by('-timestamp').first()
    
    latest_temperature = latest_entry.temprature if latest_entry else 0
    latest_humidity = latest_entry.humidity if latest_entry else 0
    
    # Calculate time since last update
    time_since_update = "No data yet"
    if latest_entry:
        diff = timezone.now() - latest_entry.timestamp
        time_since_update = humanize_time(diff)
    
    # Prepare chart data (last 24h as default)
    last_day = timezone.now() - timedelta(days=1)
    chart_entries = LogEntry.objects.filter(timestamp__gte=last_day).order_by('timestamp')
    
    timestamps = [e.timestamp.strftime("%H:%M") for e in chart_entries]
    temperature_data = [float(e.temprature) for e in chart_entries]
    humidity_data = [float(e.humidity) for e in chart_entries]
    
    # Prepare recent entries with humanized times
    recent_entries_data = []
    for entry in recent_entries:
        diff = timezone.now() - entry.timestamp
        recent_entries_data.append({
            'time': humanize_time(diff),
            'temperature': entry.temprature,
            'humidity': entry.humidity
        })
    
    context = {
        "recent_entries": recent_entries_data,
        "latest_temperature": latest_temperature,
        "latest_humidity": latest_humidity,
        "time_since_update": time_since_update,
        "timestamps": json.dumps(timestamps),
        "temperature_data": json.dumps(temperature_data),
        "humidity_data": json.dumps(humidity_data),
    }
    return render(request, "index.html", context)

def humanize_time(timedelta):
    """Convert timedelta to human-readable format"""
    seconds = int(timedelta.total_seconds())
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} min ago" if minutes == 1 else f"{minutes} mins ago"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour ago" if hours == 1 else f"{hours} hours ago"
    else:
        days = seconds // 86400
        return f"{days} day ago" if days == 1 else f"{days} days ago"