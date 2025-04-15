from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse,Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from students.models import Student
from .serializers import *
from rest_framework.decorators import api_view
from employees.models import Employee
from rest_framework import generics, mixins,viewsets
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer
from .pagination import CustomPagination
from employees.filters import EmployeeFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

@api_view(['GET','POST'])
def StudentsView(request, *args, **kwargs):
    if request.method=='GET':
        students=Student.objects.all()
        serializer=StudentSerializer(students, many=True)
        print(students)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    elif request.method=='POST':
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def StudentsDetailView(request,pk):
    try:
        students=Student.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method== "GET":
        serializer=StudentSerializer(students)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = StudentSerializer(students, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=="DELETE":
        students.delete()
        return Response(status=status.HTTP_200_OK)
    
    
# class Employees(APIView):
#     def get(self,request):
#         employees=Employee.objects.all()
#         serializer= EmployeeSerializer(employees, many=True)
#         return Response(serializer.data, status= status.HTTP_200_OK)
    
#     def post(self,request):
#         serializer= EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class EmployeeDetails(APIView):
#     def get_object(self,pk):
#         try:
#             employees= Employee.objects.get(pk=pk)
#             return employees
#         except Employee.DoesNotExist:
#             raise Http404
        
#     def get(self,request,pk):
#         employee=self.get_object(pk=pk)
#         serializer=EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         employee=self.get_object(pk)
#         serializer=EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#         employee= self.get_object(pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
'''
#mixins
class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
    
class EmployeeDetails(mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    
    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self,request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request,pk)
'''
# #Generics
# class Employees(generics.ListCreateAPIView):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer

# class EmployeeDetails(generics.RetrieveAPIView,generics.UpdateAPIView, generics.DestroyAPIView):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer
#     lookup_field='pk'
    
"""class EmployeeViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset=Employee.objects.all()
        serializer=EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def retrieve(self,request,pk=None):
        employee= get_object_or_404(Employee, pk=pk)
        serializer=EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        employee= get_object_or_404(Employee, pk=pk)
        serializer=EmployeeSerializer(Employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, pk=None):
        employee=get_object_or_404(Employee,pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    authentication_classes=[JWTAuthentication]
    # permission_classes=[AllowAny]
    # permission_classes=[IsAuthenticated]
    permission_classes=[IsAuthenticated]
    pagination_class=CustomPagination
    filterset_class=EmployeeFilter 
    
    def get_serializer_class(self):
        user = self.request.user
        if user.is_superuser:
            return EmployeeAdminSerializer
        return EmployeePublicSerializer    
    
class BlogsView(generics.ListCreateAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    filter_backends=[SearchFilter, OrderingFilter]
    search_fields=['blog_title','blog_body']
    ordering_fields=['id']
    
class CommentsView(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    
class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    lookup_field='pk'
    
class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    lookup_field='pk'
    
class RegisterUser(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username= serializer.data['username'])
            token_obj, _ = Token.objects.get_or_create(user=user)
            data = {
                'user': serializer.data,
                'token': token_obj.key
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
