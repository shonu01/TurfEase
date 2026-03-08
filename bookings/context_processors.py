from .models import Notification


def unread_notifications(request):
    if request.user.is_authenticated and not request.user.is_staff:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notification_count': count}
    return {'unread_notification_count': 0}
