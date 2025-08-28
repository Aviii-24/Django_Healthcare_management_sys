from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctor


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)


    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


    def create(self, validated_data):
        user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data.get('email', ''),
        password=validated_data['password']
        )
        return user


class PatientSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')


    class Meta:
        model = Patient
        fields = ('id', 'name', 'email', 'age', 'gender', 'owner', 'created_at', 'updated_at')


    def validate_age(self, value):
        if value <= 0:
            raise serializers.ValidationError('Age must be positive.')
        return value


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'email', 'specialty', 'years_experience', 'created_at', 'updated_at')


class PatientDoctorSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())


    class Meta:
        model = PatientDoctor
        fields = ('id', 'patient', 'doctor', 'created_at', 'updated_at')


    def validate(self, attrs):
        patient = attrs['patient']
        doctor = attrs['doctor']
        if PatientDoctor.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError('This doctor is already assigned to the patient.')
        return attrs