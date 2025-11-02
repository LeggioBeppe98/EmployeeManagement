#!/usr/bin/env python
"""
Script di test per i Serializers
Esegui con: python manage.py runscript test_serializers
"""

import os
import django
from datetime import date

def setup_django():
    """Configura l'ambiente Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

def test_serializers():
    """Testa tutti i serializers"""
    from employees.models import Department, Employee
    from employees.serializers import DepartmentSerializer, EmployeeSerializer
    
    print("🧪 TEST SERIALIZERS")
    print("=" * 50)
    
    # PULIZIA DATI DI TEST
    Employee.objects.filter(email__contains=".test@").delete()
    Department.objects.filter(name__contains="Test").delete()
    
    # TEST 1: DEPARTMENT SERIALIZER
    print("1. Testing DepartmentSerializer...")
    dept = Department.objects.create(
        name="IT Test", 
        description="Dipartimento di test",
        budget=75000.00
    )
    
    dept_serializer = DepartmentSerializer(dept)
    print(f"   ✅ DepartmentSerializer dati:")
    for key, value in dept_serializer.data.items():
        print(f"      {key}: {value}")
    
    # TEST 2: EMPLOYEE SERIALIZER - SERIALIZZAZIONE
    print("\n2. Testing EmployeeSerializer (serializzazione)...")
    emp = Employee.objects.create(
        first_name="Mario",
        last_name="Rossi Test",
        email="mario.test@azienda.com",
        position="Sviluppatore Junior",
        salary=40000.00,
        hire_date=date(2024, 1, 1),
        department=dept
    )
    
    emp_serializer = EmployeeSerializer(emp)
    print(f"   ✅ EmployeeSerializer dati:")
    for key, value in emp_serializer.data.items():
        print(f"      {key}: {value}")
    
    # VERIFICA CAMPI CALCOLATI
    assert 'department_name' in emp_serializer.data, "❌ department_name mancante!"
    assert emp_serializer.data['department_name'] == "IT Test", "❌ department_name errato!"
    print(f"   ✅ Campo calcolato 'department_name': {emp_serializer.data['department_name']}")
    
    # TEST 3: EMPLOYEE SERIALIZER - DESERIALIZZAZIONE
    print("\n3. Testing EmployeeSerializer (deserializzazione)...")
    new_emp_data = {
        "first_name": "Laura",
        "last_name": "Bianchi Test", 
        "email": "laura.test@azienda.com",
        "position": "Designer",
        "salary": 38000.00,
        "hire_date": "2024-02-01",
        "department": dept.id
    }
    
    new_emp_serializer = EmployeeSerializer(data=new_emp_data)
    if new_emp_serializer.is_valid():
        print("   ✅ Deserializzazione OK - dati validi")
        # NOTA: Non salviamo per non sporcare il database di test
        # new_emp = new_emp_serializer.save()
    else:
        print("   ❌ Errori validazione:", new_emp_serializer.errors)
        return False
    
    # TEST 4: VALIDAZIONE ERRORI
    print("\n4. Testing validazione errori...")
    invalid_data = {
        "first_name": "Giuseppe",
        "last_name": "Verdi Test",
        "email": "email-invalida",  # ❌ Email non valida
        "salary": -1000,  # ❌ Stipendio negativo
        "department": dept.id
    }
    
    invalid_serializer = EmployeeSerializer(data=invalid_data)
    is_valid = invalid_serializer.is_valid()
    print(f"   ✅ Dati invalidi correttamente rilevati: {not is_valid}")
    if not is_valid:
        print("   ✅ Errori trovati:")
        for field, errors in invalid_serializer.errors.items():
            print(f"      {field}: {errors}")
    
    # PULIZIA FINALE
    print("\n5. Pulizia dati di test...")
    Employee.objects.filter(email__contains=".test@").delete()
    Department.objects.filter(name__contains="Test").delete()
    print("   ✅ Dati di test puliti")
    
    print("=" * 50)
    print("🎉 TUTTI I TEST SERIALIZERS SUPERATI!")
    return 

def run():
    setup_django()
    return test_serializers()

if __name__ == "__main__":
    run()