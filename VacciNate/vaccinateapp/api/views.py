from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from vaccinateapp.models import User, Vaccine, UserVaccine
from .serializer import VaccinateSerializer, UserVaccineSerializer
from rest_framework import generics, status
from rest_framework.decorators import permission_classes,api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from celery.result import AsyncResult
import logging

class VaccinateAll(generics.ListCreateAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccinateSerializer

class VaccinateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccinateSerializer
    
class UserVaccinateAll(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserVaccineSerializer
    lookup_field = None  


    def get_queryset(self):
        user = self.request.user
        return UserVaccine.objects.filter(user__username=user.username) 
       
    def perform_create(self, serializer):
            user = self.request.user
            
            vaccine_id = self.request.data.get('vaccine_id')
            vaccine = Vaccine.objects.filter(id=vaccine_id).first()

            if not vaccine:
                return HttpResponseBadRequest("The specified vaccine does not exist.")

            first_date = self.request.data.get('first_date')
            first_date = datetime.strptime(first_date, '%Y-%m-%d').date() if first_date else None
            serializer.save(user=user, vaccine=vaccine, first_date=first_date)
            
            

class UserVaccineDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserVaccineSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return UserVaccine.objects.filter(user=user)

@csrf_exempt
@require_http_methods(["POST"])
@permission_classes([IsAuthenticated])
def cancel(request, id):
    object = UserVaccine.objects.get(id = id)
    print(object.status)
    object.status = "cancelled"
    object.save()
    return HttpResponse("Vaccine cancelled")
    
@csrf_exempt
@require_http_methods(["PATCH"])
@permission_classes([IsAuthenticated])
def update_date (request, id, old_date, new_date):
    object = UserVaccine.objects.get(id = id)
    new_date_DateTime = datetime.strptime(new_date, '%Y-%m-%d').date()
    if old_date not in object.all_dates:
        return HttpResponseBadRequest("The specified date does not exist.")
    if new_date_DateTime in object.all_dates:
        return HttpResponseBadRequest("The specified date already exists.")
    if new_date_DateTime < object.first_date and old_date == object.first_date:
        return HttpResponseBadRequest("The specified date is earlier than the first date.")
    if new_date_DateTime < datetime.now().date():
        return HttpResponseBadRequest("The specified date is earlier than today.")
    object.all_dates[object.all_dates.index(old_date)] = new_date
    object.save()
    return HttpResponse("Date updated")


@csrf_exempt
@require_http_methods(["PATCH"])
@permission_classes([IsAuthenticated])
def update_dose (request, id):
    object = UserVaccine.objects.get(id = id)
    object.dose += 1
    if object.dose == len(object.all_dates):
        object.status = "done"
    object.save()
    return HttpResponse("Dose updated")

class Notify(generics.RetrieveAPIView):
    
    def send_to_user(self, user_id):
        
        user = User.objects.get(id=user_id)
        devices = FCMDevice.objects.filter(user=user.id)
        devices.send_message(
            message =Message(
                notification=Notification(
                    title='Vaccine Reminder',
                    body=f'You have a vaccine appointment today'
                ),
            ),  
        )
        
        return Response("Notified", status=status.HTTP_200_OK)
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])  # use JWT authentication
@permission_classes([IsAuthenticated])
def notify_user_test(request):
    user = request.user
    notify(user.id)
    return HttpResponse("Notified")

@receiver(post_save, sender=UserVaccine)
def notify_user(sender, instance, **kwargs):
    user_id = instance.user.id
    notify.apply_async(args=[user_id], eta=datetime.now())
    for date_str in instance.all_dates[0:]:
        notify.apply_async(args=[user_id], eta=datetime.strptime(date_str, '%Y-%m-%d'))

@shared_task
def notify(user_id):
    logger = logging.getLogger(__name__)
    logger.info("Notifying user")
    try:
        Notify().send_to_user(user_id)
        logger.info("Notification sent to user %s", user_id)
    except Exception as e:
        logger.error("Error sending notification to user %s: %s", user_id, e)