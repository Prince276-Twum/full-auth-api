from django.shortcuts import render
from djoser.views import UserViewSet as BaseUserViewSet
from django.db import transaction
from django.conf import settings
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from djoser.social.views import ProviderAuthView

# Create your views here.


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            response.set_cookie(
                "access",
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE)

            response.set_cookie(
                "refresh",
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE)

        return response


class UserViewSet(BaseUserViewSet):
    def perform_create(self, serializer, *args, **kwargs):
        with transaction.atomic():
            print(settings.DJOSER)
            user = super().perform_create(serializer, *args, **kwargs)
            # context = {"user": user}
            # to = user
            # print(to)

            # try:
            #     if settings.SEND_ACTIVATION_EMAIL:
            #         settings.EMAIL.activation(self.request, context).send(to)
            #     elif settings.SEND_CONFIRMATION_EMAIL:
            #         settings.EMAIL.confirmation(self.request, context).send(to)
            # except Exception as e:
            #     # If the email fails, rollback the transaction
            #     raise ValidationError(f"Email sending failed: {str(e)}")
        return user


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            response.set_cookie(
                "access",
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE)

            response.set_cookie(
                "refresh",
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE)

        return response


class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):

        refresh_token = request.COOKIES.get("refresh")
        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get("access")

            response.set_cookie(
                "access",
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):

        access_token = request.COOKIES.get("access")

        if access_token:
            request.data["token"] = access_token

        response = super().post(request, *args, **kwargs)

        return response


class Logout(APIView):
    def post(self, request,  *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response
