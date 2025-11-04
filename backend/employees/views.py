from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer
from django.db.models import Count, Avg, Sum

@api_view(['GET'])
def dashboard_stats(request):
    """
    API per le statistiche della dashboard
    """
    # Solo utenti autenticati
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    stats = {
        'total_employees': Employee.objects.count(),
        'active_employees': Employee.objects.filter(is_active=True).count(),
        'average_salary': Employee.objects.filter(is_active=True).aggregate(
            Avg('salary')
        )['salary__avg'] or 0,
        'total_departments': Department.objects.count(),
        'total_salary_budget': Employee.objects.filter(is_active=True).aggregate(
            Sum('salary')
        )['salary__sum'] or 0,
    }
    
    # Distribuzione per dipartimento
    department_distribution = Department.objects.annotate(
        employee_count=Count('employee')
    ).values('name', 'employee_count')
    
    # Distribuzione stipendi
    salary_ranges = [
        {'range': '20k-30k', 'min': 20000, 'max': 30000},
        {'range': '30k-40k', 'min': 30000, 'max': 40000},
        {'range': '40k-50k', 'min': 40000, 'max': 50000},
        {'range': '50k-60k', 'min': 50000, 'max': 60000},
        {'range': '60k+', 'min': 60000, 'max': 999999},
    ]
    
    salary_distribution = []
    for range_obj in salary_ranges:
        count = Employee.objects.filter(
            is_active=True,
            salary__gte=range_obj['min'],
            salary__lt=range_obj['max']
        ).count()
        salary_distribution.append({
            'range': range_obj['range'],
            'count': count
        })
    
    # Ultime assunzioni
    recent_hires = Employee.objects.filter(is_active=True).order_by('-hire_date')[:5].values(
        'id', 'first_name', 'last_name', 'position', 'department__name', 'hire_date'
    )
    
    return Response({
        'stats': stats,
        'department_distribution': list(department_distribution),
        'salary_distribution': salary_distribution,
        'recent_hires': list(recent_hires)
    })

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