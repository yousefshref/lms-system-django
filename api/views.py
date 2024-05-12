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








@api_view(['GET', 'POST'])
def form_list(request):
    if request.method == 'GET':
        forms = models.Form.objects.all().order_by('-id')
        serializer = serializers.FormSerializer(forms, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = serializers.FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



@api_view(['GET', 'PUT', 'DELETE'])
def form_detail(request, pk):
    try:
        form = models.Form.objects.get(pk=pk)
    except:
        return Response({'error': 'Form not found'})

    if request.method == 'GET':
        serializer = serializers.FormSerializer(form)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = serializers.FormSerializer(form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == 'DELETE':
        form.delete()
        return Response({"success":True})




@api_view(['POST'])
def form_field_list(request):
    serializer = serializers.FormFieldSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def form_field_detail(request, pk):
    try:
        form_field = models.FormField.objects.get(pk=pk)
    except:
        return Response({'error': 'FormField not found'})
    
    if request.method == 'GET':
        serializer = serializers.FormFieldSerializer(form_field)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = serializers.FormFieldSerializer(form_field, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        form_field.delete()
        return Response({"success":True})
    







@api_view(['GET', 'POST'])
def form_answer_parent_list(request):
    if request.method == 'GET':
        form_answers = models.FormAnswerParent.objects.all().order_by('-id')

        if request.GET.get('form_id'):
            form_answers = form_answers.filter(form_id=request.GET.get('form_id'))

        serializer = serializers.FormAnswerParentSerializer(form_answers, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = serializers.FormAnswerParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



@api_view(['GET', 'PUT', 'DELETE'])
def form_answer_parent_detail(request, pk):
    try:
        form_answer = models.FormAnswerParent.objects.get(pk=pk)
    except:
        return Response({'error': 'FormAnswerParent not found'})
    
    if request.method == 'GET':
        serializer = serializers.FormAnswerParentSerializer(form_answer)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = serializers.FormAnswerParentSerializer(form_answer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        form_answer.delete()
        return Response({"success":True})






@api_view(['GET', 'POST'])
def form_answer_list(request):
    if request.method == 'GET':
        form_answers = models.FormAnswer.objects.all().order_by('-id')

        if request.GET.get('parent_id'):
            form_answers = form_answers.filter(parent_id=request.GET.get('parent_id'))

        serializer = serializers.FormAnswerSerializer(form_answers, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = serializers.FormAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    


@api_view(['GET', 'PUT', 'DELETE'])
def form_answer_detail(request, pk):
    try:
        form_answer = models.FormAnswer.objects.get(pk=pk)
    except:
        return Response({'error': 'FormAnswer not found'})
    
    if request.method == 'GET':
        serializer = serializers.FormAnswerSerializer(form_answer)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = serializers.FormAnswerSerializer(form_answer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        form_answer.delete()
        return Response({"success":True})






