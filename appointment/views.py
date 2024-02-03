from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied ,NotAcceptable
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action 
from django.shortcuts import get_object_or_404

from .permissions import IsOwnerOrReadOnly,IsDoctor
from .models import Doctor,Patient,MeetingTime
from .serializers import DoctorSerializer,CreateDoctorSerializer,PatientSerializer,MeetingTimeSerializer,BulkCreateMeetingTimeSerializer

class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.select_related('user').all()
    # serializer_class = DoctorSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateDoctorSerializer
        return DoctorSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}
    
    @action(detail=False,methods=['get','put','delete'],permission_classes=[IsAuthenticated])# permission_classes = [IsDoctor] # if this ==> get_ser_cont:doctor=d.ob.filter
    def me(self,request):
        doctor = get_object_or_404(Doctor,user=request.user) # converte to get
        if request.method == 'GET':
            print('@@@@@@GET')
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            print('@@@@@@PUT')
            print(doctor)
            serializer = DoctorSerializer(doctor,data=request.data,context={'user':request.user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        elif request.method == 'DELETE':
            doctor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
    
class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.select_related('time','doctor').all()
    # queryset = Patient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PatientSerializer

class MeetingTimeViewSet(ModelViewSet):
    # queryset = MeetingTime.objects.all()
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsDoctor] # if this ==> get_ser_cont:doctor=d.ob.filter
    serializer_class = MeetingTimeSerializer

    def get_queryset(self):
        return MeetingTime.objects.select_related('doctor__user').filter(doctor=self.request.user.id)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data,many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_serializer_context(self):
        doctor=get_object_or_404(Doctor,user=self.request.user)
        # doctor = Doctor.objects.filter(user=self.request.user)
        return {'doctor':doctor}

        
    
    
