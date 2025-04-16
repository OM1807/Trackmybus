from django.db import models



class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    ]
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


class Bus(models.Model):
    route = models.CharField(max_length=50, unique=True)
    driver = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})

    def __str__(self):
        return self.route


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensure correct relation
    route = models.CharField(max_length=100)
    stop = models.CharField(max_length=100)

    def __str__(self):
        return self.user.name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.user.name} - {self.status} ({self.date})"


class BusLocation(models.Model):
    route = models.CharField(max_length=100, default="Sangli")
    latitude = models.FloatField()
    longitude = models.FloatField()
    estimated_arrival = models.IntegerField(default=5)  # Estimated minutes to arrival
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bus on Route {self.route} at {self.latitude}, {self.longitude}"


class DriverInfo(models.Model):
    name = models.CharField(max_length=100, default="User1")
    phone = models.CharField(max_length=15, default="1234567890")
    route = models.CharField(max_length=100, default="Sangli")

    def __str__(self):
        return f"Driver {self.name} for Route {self.route}"


