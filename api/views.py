from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework.authtoken.models import Token

from api import models
from api import serializers

from django.db.models import Q

from django.http import Http404

from django.contrib.auth.models import User





@api_view(['POST'])
def signup(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
  try:
      user = User.objects.get(
          Q(email=request.data['auth']) |
          Q(student__phone_number=request.data['auth'])
      )
  except User.DoesNotExist:
      return Response({"error":"لا يوجد مستخدم بهذه البيانات"})
  
  if not user.check_password(request.data['password']):
      return Response({"error":"كلمة السر او اسم المستخدم خاطئيين"})

  token, created = Token.objects.get_or_create(user=user)
  serializer = serializers.UserSerializer(user)
  return Response({'token': token.key, 'user': serializer.data})







@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
  user = request.user
  serializer = serializers.UserSerializer(user)
  return Response(serializer.data)




@api_view(['PUT', 'DELETE'])
def user_detail(request, pk):
  user = User.objects.get(pk=pk)
  if request.method == 'PUT':
    serializer = serializers.UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)
  elif request.method == 'DELETE':
    user.delete()
    return Response({"success": True})





class LevelList(APIView):

    def get(self, request):
        levels = models.Level.objects.all()
        serializer = serializers.LevelSerializer(levels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.LevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LevelDetail(APIView):

    def get_object(self, pk):
        try:
            return models.Level.objects.get(pk=pk)
        except models.Level.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        level = self.get_object(pk)
        serializer = serializers.LevelSerializer(level)
        return Response(serializer.data)

    def put(self, request, pk):
        level = self.get_object(pk)
        serializer = serializers.LevelSerializer(level, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        level = self.get_object(pk)
        level.delete()
        return Response({'success': True})


class StudentList(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = models.Student.objects.all().order_by('-id')
        serializer = serializers.StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
      serializer = serializers.StudentSerializer(data=request.data)
      images = request.data.get('images')
      print(images)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors)


class StudentDetail(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return models.Student.objects.get(pk=pk)
        except models.Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = serializers.StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = serializers.StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentImageList(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_images = models.StudentImage.objects.filter(image__id=request.GET.get('image_id'))
        serializer = serializers.StudentImageSerializer(student_images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StudentImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentImageDetail(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return models.StudentImage.objects.get(pk=pk)
        except models.StudentImage.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        student_image = self.get_object(pk)
        serializer = serializers.StudentImageSerializer(student_image)
        return Response(serializer.data)

    def put(self, request, pk):
        student_image = self.get_object(pk)
        serializer = serializers.StudentImageSerializer(student_image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student_image = self.get_object(pk)
        student_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def create_user(username, password):
    user = User.objects.create(username=username)
    user.set_password(str(password))
    user.save()
    return user



import pandas as pd

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_students_with_excel_sheet(request):
    excel_file = request.data['file']
    df = pd.read_excel(excel_file)
    for index, row in df.iterrows():
        student = row.to_dict()
        level = models.Level.objects.get(name=student['level'])
        student['level'] = level
        
        try:
            # create user
            username = f"{str(student['full_name']).replace(' ', '_')}_{str(student['national_id_number'])[:4]}"
            password = student['national_id_number']
            user = create_user(username, password)
            student['user'] = user

            # create student profile
            student_instance = models.Student.objects.create(**student)
        except:
            pass

    return Response({"success":True})





# @api_view(['POST'])
# def signup(request):
#   serializer = serializers.UserSerializer(data=request.data)
#   if serializer.is_valid():
#     serializer.save()
#     user = models.CustomUser.objects.get(username=request.data['username'])
#     user.set_password(request.data['password'])
#     user.save()
#     token = Token.objects.create(user=user)
#     return Response({'token': token.key, 'user': serializer.data})
#   return Response(serializer.errors, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def login(request):
#   try:
#     user = models.CustomUser.objects.get(email=request.data['email'])
#   except:
#     return Response({"error":"لا يوجد مستخدم بهذه البيانات"})
#   if not user.check_password(request.data['password']):
#       return Response({"error":"كلمة السر او اسم المستخدم خاطئيين"})
#   token, created = Token.objects.get_or_create(user=user)
#   serializer = serializers.UserSerializer(user)
#   return Response({'token': token.key, 'user': serializer.data})





# @api_view(['GET'])
# def levels(request):
#   levels = models.Level.objects.all()
#   serializer = serializers.LevelSerializer(levels, many=True)
#   return Response(serializer.data)

# @api_view(['GET'])
# def subjects(request):
#   subjects = models.Subject.objects.all()
#   serializer = serializers.SubjectSerializer(subjects, many=True)
#   return Response(serializer.data) 



# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def get_school(request):
#   school = models.School.objects.get(user=request.user)
#   serializer = serializers.SchoolSerializer(school)
#   return Response(serializer.data)


# @api_view(['GET'])
# def get_student_or_parent(request):
#   phone = request.GET.get('phone')

#   if models.Student.objects.filter(
#     Q(phone=phone) | Q(parent_phone=phone)
#   ).exists():
#     student = models.Student.objects.get(phone=phone)
#     serializer = serializers.StudentSerializer(student)
#     return Response(serializer.data)
#   return Response({"notExist":True})



# def is_school(request):
#   try:
#     school = models.School.objects.get(user=request.user)
#     return True
#   except:
#     return False


# def is_teacher(request):
#   try:
#     teacher = models.Teacher.objects.get(user=request.user)
#     return True
#   except:
#     return False
  

# def is_student(request):
#   try:
#     student = models.Student.objects.get(user=request.user) 
#     return True
#   except:
#     return False



# @api_view(['POST', 'GET'])
# def profile_list(request):
#   if request.method == 'POST':
#     if request.GET.get('type') == 'student':
#       serializer = serializers.StudentSerializer(data=request.data)
#       if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)

#     if request.GET.get('type') == 'teacher':
#       serializer = serializers.TeacherSerializer(data=request.data)
#       if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
    
#     if request.GET.get('type') == 'school':
#       serializer = serializers.SchoolSerializer(data=request.data)
#       if serializer.is_valid():
#         data = serializer.save()
#         if(request.data.get('levels')):
#           data.levels.set(*request.data.get('levels').split(','))
#         if(request.data.get('subjects')):
#           data.subjects.set(*request.data.get('subjects').split(','))
#         return Response(serializer.data)
          
#     return Response(serializer.errors)



# @api_view(['PUT', 'GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def profile_detail(request):
#   if request.method == 'PUT':
#     user = models.CustomUser.objects.get(pk=request.user.pk)

#     if is_student(request):
#       profile = models.Student.objects.get(user=user)
#       serializer = serializers.StudentSerializer(profile, data=request.data, partial=True)
#       if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#       return Response(serializer.errors)    

#     if is_teacher(request):
#       profile = models.Teacher.objects.get(user=user)
#       serializer = serializers.TeacherSerializer(profile, data=request.data, partial=True)
#       if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#       return Response(serializer.errors)
    
#     if is_school(request):
#       profile = models.School.objects.get(user=user)

#       if(request.data.get('subjects')):
#         profile.subjects.set(request.data.get('subjects').split(','))

#       if(request.data.get('levels')):
#         profile.levels.set(request.data.get('levels').split(','))
      
#       serializer = serializers.SchoolSerializer(profile, data=request.data, partial=True)
#       if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#       return Response(serializer.errors)






# @api_view(['GET', 'PUT'])
# def website_list(request, user_pk):
#   if request.method == 'GET':
#     try:
#       website = models.WebSite.objects.get(user__pk=user_pk)
#     except models.WebSite.DoesNotExist:
#       website = models.WebSite.objects.create(user=models.CustomUser.objects.get(pk=user_pk))

#     return Response(serializers.WebSiteSerializer(website).data)
  
#   if request.method == 'PUT':
#     website = models.WebSite.objects.get(user__pk=user_pk)
#     serializer = serializers.WebSiteSerializer(website, data=request.data, partial=True)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)






# @api_view(['GET', 'POST'])
# # @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([AllowAny])
# def posts_list(request):
#   if request.method == 'GET':
#     posts = models.Post.objects.all().order_by('-id')
#     serializer = serializers.PostSerializer(posts, many=True)
#     return Response(serializer.data)

#   if request.method == 'POST':
#     serializer = serializers.PostSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)



# @api_view(['DELETE'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# def post_detail(request, pk):
#   try:
#     post = models.Post.objects.get(pk=pk)
#   except models.Post.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)
  
#   if request.method == 'DELETE':
#     post.delete()
#     return Response({"success":True})








# @api_view(['GET', 'POST'])
# def form_type_list(request):
#   if request.method == 'GET':
#     form_types = models.FormType.objects.all().order_by('-id')
#     serializer = serializers.FormTypeSerializer(form_types, many=True)
#     return Response(serializer.data)

#   if request.method == 'POST':
#     serializer = serializers.FormTypeSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)
  


# @api_view(['PUT', 'DELETE'])
# def form_type_detail(request, pk):
#   try:
#     form_type = models.FormType.objects.get(pk=pk)
#   except models.FormType.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)

#   if request.method == 'PUT':
#     serializer = serializers.FormTypeSerializer(form_type, data=request.data, partial=True)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)

#   if request.method == 'DELETE':
#     form_type.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)






# @api_view(['GET', 'POST'])
# def form_list(request):
#   if request.method == 'GET':
#     forms = models.Form.objects.all().order_by('-id')
#     serializer = serializers.FormSerializer(forms, many=True)
#     return Response(serializer.data)
  
#   if request.method == 'POST':
#     serializer = serializers.FormSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)



# @api_view(['GET', 'PUT', 'DELETE'])
# def form_detail(request, pk):
#   try:
#     form = models.Form.objects.get(pk=pk)
#   except models.Form.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)

#   if request.method == 'GET':
#     serializer = serializers.FormSerializer(form)
#     return Response(serializer.data)
  
#   if request.method == 'PUT':
#     serializer = serializers.FormSerializer(form, data=request.data, partial=True)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)
  
#   if request.method == 'DELETE':
#     form.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)




# @api_view(['GET', 'POST'])
# def form_field_list(request):
#   if request.method == 'GET':
#     form_fields = models.FormField.objects.all()

#     if request.GET.get('form'):
#       form_fields = form_fields.filter(form__pk=request.GET.get('form'))

#     serializer = serializers.FormFieldSerializer(form_fields, many=True)
#     return Response(serializer.data)

#   if request.method == 'POST':
#     serializer = serializers.FormFieldSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)
  


# @api_view(['GET', 'PUT', 'DELETE'])
# def form_field_detail(request, pk):
#   try:
#     form_field = models.FormField.objects.get(pk=pk)
#   except models.FormField.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)

#   if request.method == 'GET':
#     serializer = serializers.FormFieldSerializer(form_field)
#     return Response(serializer.data)

#   if request.method == 'PUT':
#     serializer = serializers.FormFieldSerializer(form_field, data=request.data, partial=True)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)
  
#   if request.method == 'DELETE':
#     form_field.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)



# import json

# @api_view(['GET', 'POST'])
# def form_application_list(request):
#   if request.method == 'GET':
#     form_applications = models.FormApplication.objects.all().order_by('-id')

#     if request.GET.get('form'):
#       form_applications = form_applications.filter(form__pk=request.GET.get('form'))
    
#     if request.GET.get('phone'):
#       form_applications = form_applications.filter(
#         Q(form_data__phone__icontains=request.GET.get('phone')) | Q(form_data__parent_phone__icontains=request.GET.get('phone'))
#       )

#     serializer = serializers.FormApplicationSerializer(form_applications, many=True)
#     return Response(serializer.data)

#   if request.method == 'POST':
#     serializer = serializers.FormApplicationSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)
  


# @api_view(['GET', 'PUT', 'DELETE'])
# def form_application_detail(request, pk):
#   try:
#     form_application = models.FormApplication.objects.get(pk=pk)
#   except models.FormApplication.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)
  
#   if request.method == 'GET':
#     serializer = serializers.FormApplicationSerializer(form_application)  
#     return Response(serializer.data)
  
#   if request.method == 'PUT':
#     serializer = serializers.FormApplicationSerializer(form_application, data=request.data, partial=True)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)
  
#   if request.method == 'DELETE':
#     form_application.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)






# @api_view(['GET', 'POST'])
# def student_list(request):
#   if request.method == 'GET':
#     students = models.Student.objects.all().order_by('-id')
#     serializer = serializers.StudentSerializer(students, many=True)
#     return Response(serializer.data)
  
#   if request.method == 'POST':
#     serializer = serializers.StudentSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)
  


# @api_view(['GET', 'PUT', 'DELETE'])
# def student_detail(request, pk):
#   try:
#     student = models.Student.objects.get(pk=pk)
#   except models.Student.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)

#   if request.method == 'GET':
#     serializer = serializers.StudentSerializer(student)
#     return Response(serializer.data)
  
#   if request.method == 'PUT':
#     serializer = serializers.StudentSerializer(student, data=request.data, partial=True)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)
  
#   if request.method == 'DELETE':
#     student.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)







