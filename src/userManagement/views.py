from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from .models import *
from .signals import *

def login(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    return LoginView.as_view(template_name='userManagement/login.html')

def get_active_users():
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            user_ids.append(user_id)
    return User.objects.filter(id__in=user_ids)

def logout_user_from_all_sessions(user):
    # Trouver toutes les sessions de cet utilisateur
    sessions = Session.objects.filter(session_key__in=[
        session.session_key for session in Session.objects.all()
        if session.get_decoded().get('_auth_user_id') == str(user.id)
    ])
    sessions.delete() 

@login_required  
def user_info_view(request):
    user = request.user 

    is_staff = user.is_staff  
    is_superuser = user.is_superuser  

    context = {
        'username': user.username,
        'email': user.email,
        'is_staff': is_staff,
        'is_superuser': is_superuser,
    }

    return render(request, 'userManagement/user_info.html', context)

def no_access_view(request):
    return render(request, 'userManagement/no_access.html')

def init_view(request):
    return render(request, 'userManagement/init.html')

def check_cancellation_prediction(trip):
    send_cancel_notification_to_staff(trip)

def send_cancel_notification_to_staff(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "staff_notifications",
        {
            'type': 'notification_message',
            'message': f'Le véhicule testa a une probabilité d\'annulation supérieure à 20% '
        }
    )
    return JsonResponse({'success': True}, status=200)

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    data = [{"id": n.id,"title": n.title ,"message": n.message, "created_at": n.created_at.strftime('%Y-%m-%d %H:%M:%S')} for n in notifications]
    return JsonResponse(data, safe=False)

def some_event_trigger(request):
    if request.user.is_authenticated:
        user = request.user 
        notification = Notification.objects.create(
            user=user,
            message="Le véhicule a une probabilité d'annulation supérieure à 20%"
        )
        notification.save()
    else:
        pass
    return JsonResponse({'success': True}, status=200)

def load_my_notification(request,notification_id):
    notification = Notification.objects.filter(user=request.user, id= notification_id).first()
    if request.POST:
        setattr(notification, "is_read", True)
        notification.save()
    return render(request, 'userManagement/my_notification.html', context={'notification': notification})
