from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("create",  views.UserViewSet)
urlpatterns = [
    re_path(r'^o/(?P<provider>\S+)/$',
            views.CustomProviderAuthView.as_view(), name="provider-auth"),
    path("jwt/create/", views.CustomTokenObtainPairView.as_view()),
    path("jwt/refresh/", views.CustomTokenRefreshView.as_view()),
    path("jwt/verify/", views.CustomTokenVerifyView.as_view()),
    path("logout/", views.Logout.as_view())

] + router.urls
