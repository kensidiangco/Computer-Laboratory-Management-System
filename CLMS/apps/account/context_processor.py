from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        return {
            'notification_count': Notification.objects.filter(receiver=request.user).filter(read=False),
            'notifications': Notification.objects.filter(receiver=request.user).order_by('-date_created'),
            'user_group': list(request.user.groups.values_list('name',flat = True))
        }
    return {}