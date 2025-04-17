from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json
from .models import User, Student, DriverInfo, Bus, BusLocation, Attendance
from .serializers import UserSerializer, StudentSerializer, DriverSerializer, BusSerializer, BusLocationSerializer, AttendanceSerializer
from datetime import timedelta
from django.utils.timezone import now





#  User API 
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#  Student API
class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

#  Driver API
class DriverListCreateView(generics.ListCreateAPIView):
    queryset = DriverInfo.objects.all()
    serializer_class = DriverSerializer

class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DriverInfo.objects.all()
    serializer_class = DriverSerializer

#  Bus API
class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

#  Bus Location API
class BusLocationListCreateView(generics.ListCreateAPIView):
    queryset = BusLocation.objects.all()
    serializer_class = BusLocationSerializer

class BusLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusLocation.objects.all()
    serializer_class = BusLocationSerializer

#  Attendance API
class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

# code for sign up user
@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        phone = data.get("phone")
        password = data.get("password")
        role = data.get("role")

        if User.objects.filter(phone=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone already exists"}, status=400)

        user = User.objects.create(name=name, phone=phone, password=password, role=role)
        return JsonResponse({"status": "success", "user_id": user.id})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def add_student_details(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        route = data.get("route")
        stop = data.get("stop")

        Student.objects.create(user_id=user_id, route=route, stop=stop)
        return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def add_driver_details(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        phone = data.get("phone")
        route = data.get("route")

        DriverInfo.objects.create(name=name, phone=phone, route=route)
        return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def register_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        password = data.get('password')
        route = data.get('route')
        stop = data.get('stop')

        if User.objects.filter(phone=phone).exists():
            return JsonResponse({'status': 'error', 'message': 'Phone number already registered'}, status=400)

        user = User.objects.create(name=name, phone=phone, password=password, role='student')
        Student.objects.create(route=route, stop=stop, user=user)  # FIXED LINE ✅

        return JsonResponse({'status': 'success', 'message': 'Student registered successfully'})



@csrf_exempt
def register_driver(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        name = data.get('name')
        phone = data.get('phone')
        password = data.get('password')
        route = data.get('route')

        # First, create the user
        user = User.objects.create(
            name=name,
            phone=phone,
            password=password,
            role='driver'
        )

        # Then, create the driver info record
        DriverInfo.objects.create(
            name=name,
            phone=phone,
            route=route
        )

        Bus.objects.create(
            route = route,
            driver_id = user
        )

        return JsonResponse({'status': 'success', 'message': 'Driver registered successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




# code for login user

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone = data.get("phone")
            password = data.get("password")
            role = data.get("role")

            print(f"Login Attempt: Phone={phone}, Password={password}, Role={role}")  # Debugging log

            user = User.objects.filter(phone=phone, password=password, role=role).first()

            if user:
                # ✅ Fetch student details if the user is a student
                student = Student.objects.filter(user=user).first()
                student_id = student.id if student else None  # Handle case where student doesn't exist
                if student:
                    print(f"Student ID Found: {student.id}")
                else:
                    print("No student record found for this user")

                response_data = {
                    "message": "Login successful",
                    "user_id": user.id,
                    "student_id": student_id,  # ✅ Include student_id in response
                    "name": user.name,
                    "role": user.role
                }
                
                # ✅ If the user is a driver, fetch their assigned route
                if user.role == "driver" or user.role == "Driver":
                    bus = Bus.objects.filter(driver=user).first()
                    response_data["route"] = bus.route if bus else "No Route Assigned"

                return JsonResponse(response_data, status=200)

            else:
                return JsonResponse({"error": "Invalid phone number, password, or role"}, status=401)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def get_driver_by_route(request, route):
    try:
        driver = DriverInfo.objects.filter(route=route).first()  # Use .first() to prevent errors
        if driver:
            return JsonResponse({
                "name": driver.name,
                "phone": driver.phone,
            })
        else:
            return JsonResponse({"error": "No driver found for this route"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# fetch student details 
def get_student(request, phone):
    try:
        user = get_object_or_404(User, phone=phone)
        student = get_object_or_404(Student, user=user)

        data = {
            "name": user.name,
            "phone": user.phone,
            "route": student.route,  # already a string
            "stop": student.stop
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)




#attendance of the student 
@csrf_exempt
def get_attendance_summary(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)

        today = now().date()
        first_day_of_current_month = today.replace(day=1)
        first_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = first_day_of_previous_month.replace(day=1)
        first_day_of_two_months_ago = first_day_of_previous_month - timedelta(days=1)
        first_day_of_two_months_ago = first_day_of_two_months_ago.replace(day=1)

        # Get attendance records for last two months
        attendance_data = (
            Attendance.objects
            .filter(student=student, status="Present", date__gte=first_day_of_two_months_ago)
            .values("date")
        )

        # Initialize attendance counts
        attendance_count = {
            first_day_of_previous_month.month: 0,
            first_day_of_two_months_ago.month: 0
        }

        # Count attendance per month
        for record in attendance_data:
            record_date = record["date"]
            if record_date.month == first_day_of_previous_month.month:
                attendance_count[first_day_of_previous_month.month] += 1
            elif record_date.month == first_day_of_two_months_ago.month:
                attendance_count[first_day_of_two_months_ago.month] += 1

        # Month Names Mapping
        month_names = {
            first_day_of_previous_month.month: first_day_of_previous_month.strftime("%B"),
            first_day_of_two_months_ago.month: first_day_of_two_months_ago.strftime("%B"),
        }

        # Prepare response
        attendance_summary = {
            month_names[month]: count for month, count in attendance_count.items()
        }

        return JsonResponse(attendance_summary, safe=False)

    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)

    
# update the student ( from admin dashboard )
@csrf_exempt  
def update_student(request, phone):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            
            user = get_object_or_404(User, phone=phone)
            student = get_object_or_404(Student, user=user)
            
            # Update User model fields
            user.name = data.get("name", user.name)
            user.phone = data.get("phone", user.phone)  # Ensure phone is unique
            user.save()

            # Update Student model fields
            student.stop = data.get("stop", student.stop)
            student.route = data.get("route", student.route)  # Fixed from `route_id`
            student.save()
            
            return JsonResponse({"message": "Student updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method. Use PUT."}, status=405)

# delte the student (from admin dashboard)
@csrf_exempt
def delete_student(request, phone):
    if request.method == "DELETE":
        try:
            user = User.objects.filter(phone=phone).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            student = Student.objects.filter(user=user).first()
            if student:
                student.delete()
            user.delete()

            return JsonResponse({"message": "Student deleted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)




