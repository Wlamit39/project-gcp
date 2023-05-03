from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from authentication.models import User, Expesaces
import json
from rest_framework.decorators import APIView
from common.exception import MissingFieldException
from common import error_codes as ec
from rest_framework.response import Response
from rest_framework import status
from django.core import cache

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
            if (phone and User.objects.filter(username=username, phone=phone, password=password).first())\ # if empty array condition is true??
                    or (email and User.objects.filter(username=username, email=email, password=password).first()):# encriypted--- need to be explored hash creation
                error = ec.WRONG_CREDENTIALS # new exception already exist
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            try:
                User.objects.create(username=username, password=password, phone=phone, email=email)
                return Response({'message': 'Signup successful'}, status=status.HTTP_200_OK)#JsonResponse({'message': 'Signup successful'})
            except Exception:
                submit_exception_on_sentry()
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
                submit_exception_on_sentry()
                error = ec.UNEXPECTED_ERROR
                return Response(error, status=status.HTTP_400_BAD_REQUEST)


class ExpenseAddView(APIView):

    def post(self,request):

        if request.method != "Post":
            error = ec.UNEXPECTED_REQUEST_METHOD
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        post_data = request.body
        decoded_data = post_data.decode('utf-8')
        data = json.loads(decoded_data)

        creater = request.user.id #the user who is adding expense
        if not creater:
            raise MissingFieldException(field_name="creator")
        user_phone = data.get('phone')# the  other user involved in expense
        if not user_phone:
            raise MissingFieldException(field_name="user_phone")
        user_id = User.objects.get(phone=user_phone).id
        amount = data.get('amount')
        title = data.get('title')
        try:
            Expesaces.objects.create(expence_amount = amount, expence_title = title,expence_creator = creater,expence_user = user_id)
            return Response({'message': 'Espence added  successful'}, status=status.HTTP_200_OK)
        except Exception:
            submit_exception_on_sentry()
            error = ec.UNEXPECTED_ERROR
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


class ExpenseEditView(APIView):

    def post(self,request):

        if request.method != "Post":
            error = ec.UNEXPECTED_REQUEST_METHOD
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        post_data = request.body
        decoded_data = post_data.decode('utf-8')
        data = json.loads(decoded_data)

        creater = request.user.id #the user who is adding expense
        if not creater:
            raise MissingFieldException(field_name="creator")
        old_user_phone = data.get('old_phone')# the  other user involved in expense
        if not old_user_phone:
            raise MissingFieldException(field_name="old_user_phone")
        old_user_id = User.objects.get(phone=old_user_phone).id
        new_user_phone = data.get('new_phone')  # the  other user involved in expense
        if not old_user_phone:
            raise MissingFieldException(field_name="new_user_phone")
        new_user_id = User.objects.get(phone=new_user_phone).id
        old_amount = data.get('old_amount')
        old_title = data.get('old_title')
        new_amount = data.get('new_amount')
        new_title = data.get('new_title')
        try:
            Old_exp = Expesaces.objects.create(expence_amount = old_amount, expence_title = old_title,expence_creator = creater,expence_user = old_user_id)
            Old_exp.expense_amount = new_amount
            Old_exp.expense_title = new_title
            Old_exp.expense_user = new_user_id
            Old_exp.save()
            return Response({'message': 'Espence modified successful'}, status=status.HTTP_200_OK)
        except Exception:
            submit_exception_on_sentry()
            error = ec.UNEXPECTED_ERROR
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDeleteView(APIView):

    def delete(self, request):

        if request.method != "Post":
            error = ec.UNEXPECTED_REQUEST_METHOD
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        post_data = request.body
        decoded_data = post_data.decode('utf-8')
        data = json.loads(decoded_data)

        creater = request.user.id  # the user who is adding expense
        if not creater:
            raise MissingFieldException(field_name="creator")
        old_user_phone = data.get('old_phone')  # the  other user involved in expense
        if not old_user_phone:
            raise MissingFieldException(field_name="old_user_phone")
        old_user_id = User.objects.get(phone=old_user_phone).id
        old_amount = data.get('old_amount')
        old_title = data.get('old_title')
        try:
            Old_exp = Expesaces.objects.get(expence_amount=old_amount, expence_title=old_title,
                                               expence_creator=creater, expence_user=old_user_id)
            Old_exp.delete()
            return Response({'message': 'Espence deleted successful'}, status=status.HTTP_200_OK)
        except Exception:
            submit_exception_on_sentry()
            error = ec.UNEXPECTED_ERROR
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

