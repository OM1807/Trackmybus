from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    StudentListCreateView, StudentDetailView,
    DriverListCreateView, DriverDetailView,
    BusListCreateView, BusDetailView,
    BusLocationListCreateView, BusLocationDetailView,
    AttendanceListCreateView, AttendanceDetailView,
    login_user,
    get_driver_by_route,
    get_student, update_student, delete_student,get_attendance_summary,signup, add_student_details, add_driver_details,
    register_driver,register_student
)

urlpatterns = [
    path('signup/',signup),
    path('student-details/',add_student_details),
    path('driver-details/', add_driver_details),
    path('register_student/', register_student, name='register_student'),
    path('register_driver/', register_driver, name='register_driver'),

    # ✅ User APIs
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # ✅ Student APIs
    path('students/', StudentListCreateView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # ✅ Driver APIs
    path('drivers/', DriverListCreateView.as_view(), name='driver-list'),
    path('drivers/<int:pk>/', DriverDetailView.as_view(), name='driver-detail'),

    # ✅ Bus APIs
    path('buses/', BusListCreateView.as_view(), name='bus-list'),
    path('buses/<int:pk>/', BusDetailView.as_view(), name='bus-detail'),

    # ✅ Bus Location APIs
    path('bus-locations/', BusLocationListCreateView.as_view(), name='bus-location-list'),
    path('bus-locations/<int:pk>/', BusLocationDetailView.as_view(), name='bus-location-detail'),

    # ✅ Attendance APIs
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance-list'),
    path('attendance/<int:pk>/', AttendanceDetailView.as_view(), name='attendance-detail'),

    #sign up APIs
    path("api/signup/", signup, name="signup"),
    #login APIs
    path("users/login/", login_user, name="login-user"),
    #get the driver information 
    path('get_driver/<str:route>/', get_driver_by_route, name='get_driver_by_route'),
    

    #fetch the student details
    path('get_student/<str:phone>/', get_student, name='get_student'),

    #attendance of the student
    path("attendance_summary/<int:student_id>/", get_attendance_summary, name="attendance_summary"),

    # update the student info 
    path("update_student/<str:phone>/", update_student, name="update_student"),


    #delete the student
    path('delete_student/<str:phone>/', delete_student, name='delete_student'),


]
