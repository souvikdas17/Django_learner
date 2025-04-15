from rest_framework import serializers
from students.models import Student
from employees.models import Employee
from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"
        
class EmployeeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields="__all__"

class EmployeePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=['emp_name']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['username', 'password']
        
    def create(self, validated_data):
        user= User.objects.create(username= validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
        
        

        
    