
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

    path('api/v1/levels/', views.levels),
    path('api/v1/subjects/', views.subjects),

    path('api/v1/check-user/', views.check_user),

    path('api/v1/profile/', views.profile_list),
    path('api/v1/profile/update/', views.profile_detail),

    path('api/v1/website/<int:user_pk>/', views.website_list),


    path('api/v1/posts/', views.posts_list),
    path('api/v1/posts/<int:pk>/', views.post_detail),



    # path('api/v1/sign-up/', views.RegisterAPI.as_view()),
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('api/v1/subjects/', views.subject_list),
    # path('api/v1/subjects/<int:pk>/', views.subject_detail),

    # path('api/v1/levels/', views.level_list),
    # path('api/v1/levels/<int:pk>/', views.level_detail),

    # path('api/v1/schools/', views.school_list),
    # path('api/v1/schools/<int:pk>/', views.school_detail),

    # path('api/v1/teachers/', views.teacher_list),
    # path('api/v1/teachers/<int:pk>/', views.teacher_detail),

    # path('api/v1/students/', views.student_list),
    # path('api/v1/students/<int:pk>/', views.student_detail),


    # path('api/v1/website/', views.website_get_or_create),
    # path('api/v1/website/update/', views.website_update),

    
    # path('api/v1/products/', views.product_list),
    # path('api/v1/products/<int:pk>/', views.product_detail),

    # path('api/v1/orders/', views.order_list),
    # path('api/v1/orders/<int:pk>/', views.order_detail),

    # path('api/v1/carts/', views.cart_list),
    # path('api/v1/carts/<int:pk>/', views.cart_detail),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
