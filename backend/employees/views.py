from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

@api_view(['GET'])
def current_user(request):
    """
    Restituisce le informazioni dell'utente corrente
    """
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email if request.user.email else '',
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser
    })

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint per gestire i dipartimenti
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint per gestire i dipendenti
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Opzionale: permette filtri aggiuntivi via query parameters
        Es: /api/employees/?department=1
        """
        queryset = Employee.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset