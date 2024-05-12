
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
    path('api/v1/students/excel/', views.send_students_with_excel_sheet),

    path('api/v1/students-images/', views.StudentImageList.as_view()),
    path('api/v1/students-images/<int:pk>/', views.StudentImageDetail.as_view()),


    path('api/v1/forms/', views.form_list),
    path('api/v1/forms/<int:pk>/', views.form_detail),

    path('api/v1/form-fields/', views.form_field_list),
    path('api/v1/form-fields/<int:pk>/', views.form_field_detail),

    path('api/v1/form-answers/', views.form_answer_parent_list),
    path('api/v1/form-answers/<int:pk>/', views.form_answer_parent_detail),

    path('api/v1/answers/', views.form_answer_list),
    path('api/v1/answers/<int:pk>/', views.form_answer_detail),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
