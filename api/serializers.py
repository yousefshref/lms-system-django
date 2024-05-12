from rest_framework import serializers
from api import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class LevelSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Level
    fields = '__all__'


class StudentImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.StudentImage
    fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    level_details = LevelSerializer(source='level', read_only=True)
    images_details = StudentImageSerializer(source='images', many=True, read_only=True)
    class Meta:
        model = models.Student
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
  student_detail = StudentSerializer(source='student', read_only=True)
  class Meta:
    model = User
    fields = '__all__'





class FormFieldSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.FormField
    fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
  form_fields = FormFieldSerializer(source='fields', many=True, read_only=True)
  class Meta:
    model = models.Form
    fields = '__all__'



class FormAnswerSerializer(serializers.ModelSerializer):
  field_details = FormFieldSerializer(source='field', read_only=True)
  class Meta:
    model = models.FormAnswer
    fields = '__all__'

class FormAnswerParentSerializer(serializers.ModelSerializer):
  form_details = FormSerializer(source='form', read_only=True)
  user_details = UserSerializer(source='user', read_only=True)
  answers_details = FormAnswerSerializer(source='answers', many=True, read_only=True)
  class Meta:
    model = models.FormAnswerParent
    fields = '__all__'


