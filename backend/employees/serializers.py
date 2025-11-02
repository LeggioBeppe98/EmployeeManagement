from rest_framework import serializers
from .models import Department, Employee

class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.ReadOnlyField()
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'budget', 'employee_count', 'created_at', 'updated_at']


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 
            'position', 'salary', 'hire_date', 'is_active',
            'department', 'department_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']