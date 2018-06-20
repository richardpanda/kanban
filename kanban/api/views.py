import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


def generate_jwt(id):
    return jwt.encode({"id": id}, settings.JWT_SECRET, algorithm="HS256").decode()


class SignUp(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = User(username=username, password=make_password(password))
        user.save()
        return Response(
            {"token": generate_jwt(user.id)}, status=status.HTTP_201_CREATED
        )
