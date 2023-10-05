from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scorehive_server.common import custom_errors

from .serializer import ScoreSerializer
from .validations import CustomException, validate_request

# Create your views here.


class ScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validate_request(request.data)
        except CustomException as e:
            return Response(
                {"error_code": e.error_code, "message": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serialized_data = ScoreSerializer(data=request.data, many=True)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({"message": "Score saved"})
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
