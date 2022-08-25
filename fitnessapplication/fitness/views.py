from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializer import TraineeRegisterSerializer, TraineeLoginSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

class TraineeRegisterAPIView(CreateAPIView):
    serializer_class=TraineeRegisterSerializer

class TraineeLoginAPIView(APIView):
    serializer_class = TraineeLoginSerializer

    def post(self, request):
        my_data = request.data
        serializer = TraineeLoginSerializer(data=my_data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
# Create your views here.
