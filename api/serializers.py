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
  levels = serializers.PrimaryKeyRelatedField(
    many=True,
    queryset=models.Level.objects.all(),
    required=False
)
  class Meta:
    model = models.Form
    fields = '__all__'
    
  def create(self, validated_data):
    levels_data = validated_data.pop('levels', [])
    form_answer_parent = models.Form.objects.create(**validated_data)
    form_answer_parent.levels.set(levels_data)
    return form_answer_parent



class FormAnswerSerializer(serializers.ModelSerializer):
  field_details = FormFieldSerializer(source='field', read_only=True)
  class Meta:
    model = models.FormAnswer
    fields = '__all__'

class FormAnswerParentSerializer(serializers.ModelSerializer):
  form_details = FormSerializer(source='form', read_only=True, required=False)
  user_details = UserSerializer(source='user', read_only=True, required=False)
  answers_details = FormAnswerSerializer(source='answers', many=True, read_only=True, required=False)
  class Meta:
    model = models.FormAnswerParent
    fields = '__all__'




