from rest_framework import serializers
from api import models
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.CustomUser
    fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Level
        fields = '__all__'



class SchoolSerializer(serializers.ModelSerializer):
  user_details = UserSerializer(source='user', read_only=True)
  level_details = LevelSerializer(source='levels', many=True, read_only=True)
  subject_details = SubjectSerializer(source='subjects', many=True, read_only=True)

  subjects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
  levels = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
  class Meta:
    model = models.School
    fields = '__all__'



class WebSiteSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.WebSite
    fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Post
    fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'


