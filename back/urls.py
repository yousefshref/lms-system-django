
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api import views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/signup/', views.signup),
    path('api/v1/login/', views.login),

    path('api/v1/user/', views.get_user),

    path('api/v1/users/<int:pk>/', views.user_detail),

    path('api/v1/levels/', views.LevelList.as_view()),
    path('api/v1/levels/<int:pk>/', views.LevelDetail.as_view()),

    path('api/v1/students/', views.StudentList.as_view()),
    path('api/v1/students/<int:pk>/', views.StudentDetail.as_view()),

    path('api/v1/students-images/', views.StudentImageList.as_view()),
    path('api/v1/students-images/<int:pk>/', views.StudentImageDetail.as_view()),

    # path('api/v1/levels/', views.levels),
    # path('api/v1/subjects/', views.subjects),

    # path('api/v1/school/', views.get_school),
    # path('api/v1/student/', views.get_student_or_parent),

    # path('api/v1/profile/', views.profile_list),
    # path('api/v1/profile/update/', views.profile_detail),

    # path('api/v1/website/<int:user_pk>/', views.website_list),


    # path('api/v1/posts/', views.posts_list),
    # path('api/v1/posts/<int:pk>/', views.post_detail),

    
    # path('api/v1/form-types/', views.form_type_list),
    # path('api/v1/form-type/<int:pk>/', views.form_type_detail),

    # path('api/v1/forms/', views.form_list),
    # path('api/v1/form/<int:pk>/', views.form_detail),

    # path('api/v1/form-fields/', views.form_field_list),
    # path('api/v1/form-field/<int:pk>/', views.form_field_detail),

    # path('api/v1/form-applications/', views.form_application_list),
    # path('api/v1/form-application/<int:pk>/', views.form_application_detail),


    # path('api/v1/students/', views.student_list),
    # path('api/v1/student/<int:pk>/', views.student_detail)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
