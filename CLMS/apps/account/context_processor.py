from .models import Notification
from datetime import datetime

def notification_count(request):
    if request.user.is_authenticated:
        return {
            'notification_count': Notification.objects.filter(receiver=request.user, read=False),
            'notification_read': Notification.objects.filter(receiver=request.user, read=True),
            'notifications': Notification.objects.filter(receiver=request.user).order_by('-date_created')[:3],
            'user_group': list(request.user.groups.values_list('name',flat = True)),
            'date_today': datetime.today().strftime('%B %d, %Y %H:%M:%p')
        }
    return {}