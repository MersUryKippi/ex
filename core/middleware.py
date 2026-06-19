import threading
from django.conf import settings

class MetricsMiddleware:
    _lock = threading.Lock()
    total = 0
    count_2xx = 0
    count_4xx = 0
    count_5xx = 0

    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = getattr(settings, "METRICS_LOG_FILE", None)

    def __call__(self, request):
        response = self.get_response(request)
        status = response.status_code
        
        with self._lock:
            MetricsMiddleware.total += 1
            if 200 <= status < 300:
                MetricsMiddleware.count_2xx += 1
            elif 400 <= status < 500:
                MetricsMiddleware.count_4xx += 1
            elif 500 <= status < 600:
                MetricsMiddleware.count_5xx += 1
                
            line = f"[metrics] total={MetricsMiddleware.total} 2xx={MetricsMiddleware.count_2xx} 4xx={MetricsMiddleware.count_4xx} 5xx={MetricsMiddleware.count_5xx}"
            
        print(line)
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            except Exception:
                pass
                
        return response
