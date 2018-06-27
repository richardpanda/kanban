from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserSerializer


class SignUp(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response(
                {"token": user.generate_jwt()}, status=status.HTTP_201_CREATED
            )
        else:
            errors = [
                dict(field=field, message=detail[0])
                for field, detail in user_serializer.errors.items()
            ]
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
