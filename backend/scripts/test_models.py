#!/usr/bin/env python
"""
Script di test per i modelli Employee e Department
Esegui con: python manage.py runscript test_models

"""

import os
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from employees.models import Department, Employee

def run():
    """Funzione principale eseguita dallo script"""
    print("TEST MODELLI DJANGO")
    print("=" * 50)
    
    # 1. PULIZIA DATI ESISTENTI (opzionale - solo per test)
    print("1. Pulizia dati esistenti")
    Employee.objects.all().delete()
    Department.objects.all().delete()
    
    # 2. CREAZIONE DIPARTIMENTO
    print("2. Creazione dipartimento IT")
    it_dept = Department(
        name="IT", 
        description="Dipartimento Tecnologico", 
        budget=150000.00
    )
    it_dept.save()
    print(f"   ✅ Creato: {it_dept} (Budget: €{it_dept.budget:,.2f})")
    
    # 3. CREAZIONE DIPENDENTE
    print("3. Creazione dipendente...")
    emp = Employee(
        department=it_dept,
        first_name="Mario",
        last_name="Rossi", 
        email="mario.rossi@azienda.com",
        phone="+39 123 456 7890",
        position="Senior Developer",
        salary=55000.00,
        hire_date=date(2023, 6, 15)
    )
    emp.save()
    print(f"   ✅ Creato: {emp} - {emp.position}")
    
    # 4. VERIFICHE
    print("4. Verifiche finali...")
    dept_count = Department.objects.count()
    emp_count = Employee.objects.count()
    
    print(f"   📊 Dipartimenti nel DB: {dept_count}")
    print(f"   👥 Dipendenti nel DB: {emp_count}")
    
    # 5. TEST QUERIES
    print("5. Test query avanzate...")
    employees = Employee.objects.all()
    for e in employees:
        print(f"   👤 {e.first_name} {e.last_name} - {e.department.name} - €{e.salary:,.2f}")
    
    print("=" * 50)
    print("🎉 TEST COMPLETATO CON SUCCESSO!")
    
    return {
        'departments': dept_count,
        'employees': emp_count
    }

# 1. Se lo eseguo con: python scripts/test_models.py → funziona
# 2. Se lo importo in altri test → non parte automaticamente
# 3. Se lo eseguo con: python manage.py runscript test_models → 
#    django-extensions gestisce l'esecuzione
if __name__ == "__main__":
    run()