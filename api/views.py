from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token

from api import models
from api import serializers






@api_view(['POST'])
def signup(request):
  serializer = serializers.UserSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    user = models.CustomUser.objects.get(username=request.data['username'])
    user.set_password(request.data['password'])
    user.save()
    token = Token.objects.create(user=user)
    return Response({'token': token.key, 'user': serializer.data})
  return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
  try:
    user = models.CustomUser.objects.get(email=request.data['email'])
  except:
    return Response({"error":"لا يوجد مستخدم بهذه البيانات"})
  if not user.check_password(request.data['password']):
      return Response({"error":"كلمة السر او اسم المستخدم خاطئيين"})
  token, created = Token.objects.get_or_create(user=user)
  serializer = serializers.UserSerializer(user)
  return Response({'token': token.key, 'user': serializer.data})





@api_view(['GET'])
def levels(request):
  levels = models.Level.objects.all()
  serializer = serializers.LevelSerializer(levels, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def subjects(request):
  subjects = models.Subject.objects.all()
  serializer = serializers.SubjectSerializer(subjects, many=True)
  return Response(serializer.data) 





@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_user(request):
  try:
    school = models.School.objects.get(user=request.user)
    return Response({'school': serializers.SchoolSerializer(school).data})
  except:
    pass

  try:
    teacher = models.Teacher.objects.get(user=request.user)
    return Response({'teacher': serializers.TeacherSerializer(teacher).data})
  except:
    pass

  try:
    student = models.Student.objects.get(user=request.user)
    return Response({'student': serializers.StudentSerializer(student).data})
  except:
    pass

  return Response({'error': 'User not found'})


def is_school(request):
  try:
    school = models.School.objects.get(user=request.user)
    return True
  except:
    return False


def is_teacher(request):
  try:
    teacher = models.Teacher.objects.get(user=request.user)
    return True
  except:
    return False
  

def is_student(request):
  try:
    student = models.Student.objects.get(user=request.user) 
    return True
  except:
    return False



@api_view(['POST', 'GET'])
def profile_list(request):
  if request.method == 'POST':
    if request.GET.get('type') == 'student':
      serializer = serializers.StudentSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    if request.GET.get('type') == 'teacher':
      serializer = serializers.TeacherSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    if request.GET.get('type') == 'school':
      serializer = serializers.SchoolSerializer(data=request.data)
      if serializer.is_valid():
        data = serializer.save()
        if(request.data.get('levels')):
          data.levels.set(*request.data.get('levels').split(','))
        if(request.data.get('subjects')):
          data.subjects.set(*request.data.get('subjects').split(','))
        return Response(serializer.data)
          
    return Response(serializer.errors)



@api_view(['PUT', 'GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile_detail(request):
  if request.method == 'PUT':
    user = models.CustomUser.objects.get(pk=request.user.pk)

    if is_student(request):
      profile = models.Student.objects.get(user=user)
      serializer = serializers.StudentSerializer(profile, data=request.data, partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors)    

    if is_teacher(request):
      profile = models.Teacher.objects.get(user=user)
      serializer = serializers.TeacherSerializer(profile, data=request.data, partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors)
    
    if is_school(request):
      profile = models.School.objects.get(user=user)

      if(request.data.get('subjects')):
        profile.subjects.set(request.data.get('subjects').split(','))

      if(request.data.get('levels')):
        profile.levels.set(request.data.get('levels').split(','))
      
      serializer = serializers.SchoolSerializer(profile, data=request.data, partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors)






@api_view(['GET', 'PUT'])
def website_list(request, user_pk):
  if request.method == 'GET':
    try:
      website = models.WebSite.objects.get(user__pk=user_pk)
    except models.WebSite.DoesNotExist:
      website = models.WebSite.objects.create(user=models.CustomUser.objects.get(pk=user_pk))

    return Response(serializers.WebSiteSerializer(website).data)
  
  if request.method == 'PUT':
    website = models.WebSite.objects.get(user__pk=user_pk)
    serializer = serializers.WebSiteSerializer(website, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)






@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def posts_list(request):
  if request.method == 'GET':
    posts = models.Post.objects.all().order_by('-id')
    serializer = serializers.PostSerializer(posts, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.PostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)



@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def post_detail(request, pk):
  try:
    post = models.Post.objects.get(pk=pk)
  except models.Post.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'DELETE':
    post.delete()
    return Response({"success":True})









# class RegisterAPI(APIView):
#     permission_classes = []
#     serializer_class = serializers.UserSerializer

#     def post(self, request, format=None):
#       serializer = self.serializer_class(data=request.data)
#       if serializer.is_valid():
#           user = serializer.save()
#           user.set_password(serializer.validated_data['password'])
#           user.save()
#           return Response(serializer.data)
#       return Response(serializer.errors)




# @api_view(['GET'])
# # @authentication_classes([SessionAuthentication, TokenAuthentication])
# # @permission_classes([IsAuthenticated])
# def check_user(request):
#   try:
#     school = models.School.objects.get(user=request.user)
#     return Response({'school': serializers.SchoolSerializer(school).data})
#   except:
#     pass

#   try:
#     teacher = models.Teacher.objects.get(user=request.user)
#     return Response({'teacher': serializers.TeacherSerializer(teacher).data})
#   except:
#     pass

#   try:
#     student = models.Student.objects.get(user=request.user)
#     return Response({'student': serializers.StudentSerializer(student).data})
#   except:
#     pass

#   return Response({'error': 'User not found'})




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





@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def school_list(request):
  if request.method == 'GET':
    school = models.School.objects.get(user=request.user)
    serializer = serializers.SchoolSerializer(school)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = serializers.SchoolSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def school_detail(request, pk):
  try:
    school = models.School.objects.get(pk=pk)
  except models.School.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer = serializers.SchoolSerializer(school)
    return Response(serializer.data)
  
  elif request.method == 'PUT':
    serializer = serializers.SchoolSerializer(school, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)
  
  elif request.method == 'DELETE':
    school.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)






@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_list(request):
  if request.method == 'GET':
    teachers = models.Teacher.objects.all()
    serializer = serializers.TeacherSerializer(teachers, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = serializers.TeacherSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def teacher_detail(request, pk):
  try:
    teacher = models.Teacher.objects.get(pk=pk)
  except models.Teacher.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer = serializers.TeacherSerializer(teacher)
    return Response(serializer.data)
  
  elif request.method == 'PUT':
    serializer = serializers.TeacherSerializer(teacher, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)
  
  elif request.method == 'DELETE':
    teacher.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def student_list(request):
  if request.method == 'GET':
    students = models.Student.objects.all()
    serializer = serializers.StudentSerializer(students, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = serializers.StudentSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def student_detail(request, pk):
  try:
    student = models.Student.objects.get(pk=pk)
  except models.Student.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer = serializers.StudentSerializer(student)
    return Response(serializer.data)
  
  elif request.method == 'PUT':
    serializer = serializers.StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)
  
  elif request.method == 'DELETE':
    student.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)






@api_view(['GET'])
def website_get_or_create(request):
  if request.method == 'GET':
    pk = request.GET.get('pk', None)
    try:
      if pk:
        website = models.WebSite.objects.get(user__pk=pk)
      else:
        website = models.WebSite.objects.get(user__pk=request.user.pk)
    except models.WebSite.DoesNotExist:
      if not pk:
        website = models.WebSite.objects.create(user=request.user)

    serializer = serializers.WebSiteSerializer(website)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def website_update(request):
  if request.method == 'PUT':
    website = models.WebSite.objects.get(user__pk=request.user.pk)
    serializer = serializers.WebSiteSerializer(website, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)






@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list(request):
  if request.method == 'GET':
    products = models.Product.objects.all()
    serializer = serializers.ProductSerializer(products, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = serializers.ProductSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
  try:
    product = models.Product.objects.get(pk=pk)
  except models.Product.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer = serializers.ProductSerializer(product)
    return Response(serializer.data)
  
  elif request.method == 'PUT':
    serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)
  
  elif request.method == 'DELETE':
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list(request):
  if request.method == 'GET':
    orders = models.Order.objects.all()
    serializer = serializers.OrderSerializer(orders, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = serializers.OrderSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
  try:
    order = models.Order.objects.get(pk=pk)
  except models.Order.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer = serializers.OrderSerializer(order)
    return Response(serializer.data)
  
  elif request.method == 'PUT':
    serializer = serializers.OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)
  
  elif request.method == 'DELETE':
    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_list(request):
  if request.method == 'GET':
    carts = models.Cart.objects.filter(user=request.user)
    serializer = serializers.CartSerializer(carts, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = serializers.CartSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_detail(request, pk):
  try:
    cart = models.Cart.objects.get(pk=pk)
  except models.Cart.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializers.CartSerializer(cart)
    return Response(serializer.data)

  elif request.method == 'PUT':
    serializer = serializers.CartSerializer(cart, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)

  elif request.method == 'DELETE':
    cart.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



