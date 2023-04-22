from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from authentication.models import User
import json
from rest_framework.decorators import APIView
from common.exception import MissingFieldException
from common import error_codes as ec
from rest_framework.response import Response
from rest_framework import status

class UserSignupView(APIView):

    def post(self,request):
        if request.method != 'POST':
            error = ec.UNEXPECTED_REQUEST_METHOD
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == "POST":
            post_data = request.body
            decoded_data = post_data.decode('utf-8')
            data = json.loads(decoded_data)
            username = data.get('username')
            if not username:
                raise MissingFieldException(field_name='username')
            email = data.get('email')
            phone = data.get('phone')
            if not email and not phone:
                raise MissingFieldException(message = "phone or email_id is needed")
            password = data.get('password')
            if not password:
                raise MissingFieldException(field_name="password")
            try:
                User.objects.create(username=username, password=password, phone=phone, email=email)
                return Response({'message': 'Signup successful'}, status=status.HTTP_200_OK)#JsonResponse({'message': 'Signup successful'})
            except Exception:
                error = ec.UNEXPECTED_ERROR
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):

    def get(self,request):
        if request.method != 'GET':
            error = ec.UNEXPECTED_REQUEST_METHOD
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == "GET":
            data = request.query_params
            email = data.get('email')
            phone = data.get('phone')
            username = data.get('username')
            password = data.get('password')
            if not password:
                raise MissingFieldException(field_name="password")
            if not email and not phone and not username:
                raise MissingFieldException(message='please provide correct account details')
            try:
                if email and User.objects.filter(email=email, password=password):
                    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                if phone and User.objects.filter(phone=phone, password=password):
                    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                if username and User.objects.filter(username=username, password=password):
                    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            except Exception:
                error = ec.UNEXPECTED_ERROR
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

