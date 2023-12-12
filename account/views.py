from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from account.models import User
from account.serializers import UserSerializer
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics
# from .serializers import RegisterSerializer


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer

# 로그인
class UserLoginAPI(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        # 만약 username에 맞는 user가 존재하지 않는다면
        if user is None:
            return Response(
                {"message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호가 틀린 경우
        if not check_password(password, user.password):
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # user가 맞다면
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)  # refresh 토큰 생성
            refresh_token = str(token)  # refresh 토큰 문자열
            access_token = str(token.access_token)  # access 토큰 문자열
            response = Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "login success",
                    "jwt_token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )

            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else:
            return Response(
                {"message": "로그인에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃
class LogoutAPIView(APIView):

    def post(self, request):
        logout(request)
        response = Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


# 비밀번호만 수정
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,):
        user = request.user
        new_password = request.data.get('new_password')
        user.password = make_password(new_password)
        user.save()
        return Response({'message': '비밀번호가 변경되었습니다.'}, status=status.HTTP_200_OK)
