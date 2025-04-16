from rest_framework import serializers
from .models import User, Student, DriverInfo, Bus, BusLocation, Attendance

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

# Driver Serializer
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverInfo
        fields = '__all__'

# Bus Serializer
class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

# Bus Location Serializer
class BusLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusLocation
        fields = '__all__'

# Attendance Serializer
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
