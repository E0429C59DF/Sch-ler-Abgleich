from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher, Attendance
from datetime import datetime, timedelta

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "login.html", {
                "error": "Ungültige Login-Daten"
            })

        login(request, user)

        # ADMIN
        if user.is_superuser:
            return redirect("admin_dashboard")

        # STUDENT CHECK
        if Student.objects.filter(user=user).exists():
            return redirect("student_dashboard")

        # TEACHER CHECK
        if Teacher.objects.filter(user=user).exists():
            return redirect("teacher_dashboard")

        logout(request)
        return render(request, "login.html", {
            "error": "Kein Profil (Student/Teacher) gefunden"
        })

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def student_dashboard(request):

    student = Student.objects.filter(user=request.user).first()

    if not student:
        return render(request, "error.html", {
            "message": "Kein Schüler-Profil gefunden"
        })

    thirty_days_ago = datetime.now().date() - timedelta(days=30)

    attendance_records = Attendance.objects.filter(
        student=student,
        datum__gte=thirty_days_ago
    ).order_by("-datum")

    total_classes = attendance_records.count()
    present = attendance_records.filter(anwesend=True).count()
    absent = total_classes - present

    attendance_rate = (present / total_classes * 100) if total_classes else 0

    return render(request, "student_dashboard.html", {
        "student": student,
        "attendance_records": attendance_records[:10],
        "total_classes": total_classes,
        "present": present,
        "absent": absent,
        "attendance_rate": round(attendance_rate, 1),
    })

@login_required(login_url="login")
def teacher_dashboard(request):

    teacher = Teacher.objects.filter(user=request.user).first()

    if not teacher:
        return render(request, "error.html", {
            "message": "Kein Lehrer-Profil gefunden"
        })

    students = Student.objects.filter(
        attendance__teacher=teacher
    ).distinct()

    today = datetime.now().date()

    today_attendance = Attendance.objects.filter(
        teacher=teacher,
        datum=today
    ).select_related("student")

    return render(request, "teacher_dashboard.html", {
        "teacher": teacher,
        "students": students,
        "today_attendance": today_attendance,
    })

@login_required(login_url="login")
def admin_dashboard(request):

    if not request.user.is_superuser:
        return render(request, "error.html", {
            "message": "Zugriff verweigert"
        })

    return render(request, "admin_dashboard.html", {
        "total_students": Student.objects.count(),
        "total_teachers": Teacher.objects.count(),
        "total_attendance": Attendance.objects.count(),
        "recent_attendance": Attendance.objects.select_related(
            "student", "teacher"
        ).order_by("-datum")[:10],
    })

@login_required(login_url="login")
def index(request):

    if request.user.is_superuser:
        return redirect("admin_dashboard")

    if Student.objects.filter(user=request.user).exists():
        return redirect("student_dashboard")

    if Teacher.objects.filter(user=request.user).exists():
        return redirect("teacher_dashboard")

    return redirect("login")