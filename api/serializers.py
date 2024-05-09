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




# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Subject
#         fields = '__all__'


# class LevelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Level
#         fields = '__all__'



# class SchoolSerializer(serializers.ModelSerializer):
#   user_details = UserSerializer(source='user', read_only=True)
#   level_details = LevelSerializer(source='levels', many=True, read_only=True)
#   subject_details = SubjectSerializer(source='subjects', many=True, read_only=True)

#   subjects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#   levels = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#   class Meta:
#     model = models.School
#     fields = '__all__'



# class WebSiteSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = models.WebSite
#     fields = '__all__'


# class PostSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = models.Post
#     fields = '__all__'






# class FormTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.FormType
#         fields = '__all__'


# class FormSerializer(serializers.ModelSerializer):
#     form_type_details = FormTypeSerializer(source='form_type', read_only=True)
#     class Meta:
#         model = models.Form
#         fields = '__all__'


# class FormFieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.FormField
#         fields = '__all__'


# class FormApplicationSerializer(serializers.ModelSerializer):
#     form_details = FormSerializer(source='form', read_only=True)
#     class Meta:
#         model = models.FormApplication
#         fields = '__all__'






# class TeacherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Teacher
#         fields = '__all__'


# class StudentSerializer(serializers.ModelSerializer):
#     levels_details = LevelSerializer(source='levels', many=True, read_only=True)
#     class Meta:
#         model = models.Student
#         fields = '__all__'


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Product
#         fields = '__all__'


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Order
#         fields = '__all__'


# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Cart
#         fields = '__all__'


