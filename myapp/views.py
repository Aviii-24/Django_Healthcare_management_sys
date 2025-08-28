from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Patient, Doctor, PatientDoctor
from .serializers import (
    RegisterSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorSerializer,
)
from .permissions import IsOwnerOrReadOnly

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Only patients created by the logged-in user
        return Patient.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    # anyone can read; only authenticated can modify
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class PatientDoctorViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctor.objects.all()
    serializer_class = PatientDoctorSerializer

    def get_permissions(self):
        # assigning/removing mappings requires auth
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    # Custom action: Get all doctors assigned to a specific patient
    @action(detail=False, methods=['get'], url_path=r'patient/(?P<patient_id>[^/.]+)')
    def by_patient(self, request, patient_id=None):
        mappings = PatientDoctor.objects.filter(patient_id=patient_id)
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)
