from django.db import models
from django.contrib.auth.models import User
from django.db.models import F

from django.contrib.auth.models import AbstractUser



class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



gender = (
    ('ذكر', 'ذكر'),
    ('انثى', 'انثى'),
)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    national_id_number = models.CharField(max_length=255)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='students')
    address = models.CharField(max_length=255, null=True, blank=True)
    father_phone = models.CharField(max_length=255, null=True, blank=True)
    mother_phone = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=gender, max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.full_name) + " " + str(self.pk)
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)



class StudentImage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='images/students/', blank=True, null=True)

    def __str__(self):
        return self.name






class Form(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    levels = models.ManyToManyField(Level, null=True, blank=True)
    is_student_information = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)
    


types = (
    ('text', 'text'),
    ('number', 'number'),
    ('date', 'date'),
    ('checkbox', 'checkbox'),
    ('textarea', 'textarea'),
    ('image', 'image'),
    ('time', 'time'),
)

class FormField(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=255)
    type = models.CharField(choices=types, max_length=255)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)



class FormAnswerParent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.form)


class FormAnswer(models.Model):
    parent = models.ForeignKey(FormAnswerParent, on_delete=models.CASCADE, related_name='answers', null=True)
    field = models.ForeignKey(FormField, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.parent)




