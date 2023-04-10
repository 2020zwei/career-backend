from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .models import User,Student, School
from .serializers import SignupUserSerializer,UserSerializer,SchoolSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


class SignupUser(GenericAPIView):
    permission_classes = []
    def post(self, request):
        try:
            user_data=request.data
            email=request.data.get('email')
            password=request.data.get('password')
            user = User.objects.create(email=email,  password = make_password(password))
            school = School.objects.get(id=request.data.get('school'))
            if user:
                email=request.data.get('email')
                password=request.data.get('password')
                full_name=request.data.get('full_name')
                school=school
                dob=request.data.get('dob')
                city=request.data.get('city')
                country=request.data.get('country')
                address=request.data.get('address')
                eircode=request.data.get('eircode')
                profile_image=request.data.get('profile_image')


                std=Student.objects.create(user=user, full_name=full_name,school=school,dob=dob,city=city,country=country,address=address,eircode=eircode,profile_image=profile_image)
                std.save()


            else:
                    return Response("Student already exist") 
            user.is_active = True
            user.save()
            return Response(data={'success': True}, status=status.HTTP_200_OK) 
        
        except Exception as e:
           return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)




class UserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        try:
            queryset=Student.objects.get(id=self.request.user.student.id)
            return queryset
        except Exception as e:
            raise ValidationError(e)


class SchoolView(CreateAPIView):
    permission_classes=[]
    serializer_class = SchoolSerializer

    def get(self, request):
        """Fetch All Tests By User"""
        try:
            schools=School.objects.all()
            serializer = SchoolSerializer(schools, many=True)
            return Response({'data':serializer.data, 'success':True})
    
        except Exception as e:
           return Response({'message': str(e)},success=False, status=status.HTTP_400_BAD_REQUEST)