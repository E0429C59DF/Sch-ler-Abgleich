from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")

    matrikelnummer = models.CharField(max_length=50, unique=True)
    klasse = models.CharField(max_length=50)

    geburtsdatum = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    telefon = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher")

    personalnummer = models.CharField(max_length=50, unique=True)
    fachbereich = models.CharField(max_length=100)

    zimmer = models.CharField(max_length=50, blank=True)
    telefon = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    datum = models.DateField()
    anwesend = models.BooleanField(default=True)

    notizen = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "teacher", "datum")
        ordering = ["-datum"]

    def __str__(self):
        status = "Anwesend" if self.anwesend else "Abwesend"
        return f"{self.student} - {self.datum} - {status}"