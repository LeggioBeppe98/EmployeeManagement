#!/usr/bin/env python
"""
Script di test per l'API Dashboard
Esegui con: python manage.py runscript test_dashboard_api
"""

import os
import django
import requests
import json

def setup_django():
    """Configura l'ambiente Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

def test_dashboard_api():
    """Testa l'API dashboard con autenticazione JWT"""
    
    print("🧪 TEST API DASHBOARD")
    print("=" * 50)
    
    # 1. PRIMA OTTIENI UN TOKEN JWT
    print("1. Ottenimento token JWT...")
    auth_url = "http://localhost:8000/api/token/"
    auth_data = {
        "username": "admin",
        "password": "pw_3112_tk"  # USA LA TUA PASSWORD
    }
    
    try:
        auth_response = requests.post(auth_url, json=auth_data)
        
        if auth_response.status_code != 200:
            print(f"   ❌ Errore autenticazione: {auth_response.status_code}")
            print(f"   Messaggio: {auth_response.text}")
            return False
        
        token_data = auth_response.json()
        access_token = token_data['access']
        print("   ✅ Token ottenuto con successo")
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Errore di connessione: {e}")
        return False
    
    # 2. TEST API DASHBOARD
    print("\n2. Test API Dashboard...")
    dashboard_url = "http://localhost:8000/api/dashboard/stats/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(dashboard_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ API Dashboard funziona!")
            
            # Stampa i risultati in modo leggibile
            print("\n   📊 STATISTICHE:")
            stats = data['stats']
            print(f"      • Dipendenti totali: {stats['total_employees']}")
            print(f"      • Dipendenti attivi: {stats['active_employees']}")
            print(f"      • Stipendio medio: €{stats['average_salary']:,.2f}")
            print(f"      • Dipartimenti totali: {stats['total_departments']}")
            print(f"      • Budget stipendi totale: €{stats['total_salary_budget']:,.2f}")
            
            print("\n   🏢 DISTRIBUZIONE DIPARTIMENTI:")
            for dept in data['department_distribution']:
                print(f"      • {dept['name']}: {dept['employee_count']} dipendenti")
            
            print("\n   💰 DISTRIBUZIONE STIPENDI:")
            for salary in data['salary_distribution']:
                print(f"      • {salary['range']}: {salary['count']} dipendenti")
            
            print("\n   👥 ULTIME ASSUNZIONI:")
            for hire in data['recent_hires']:
                name = f"{hire['first_name']} {hire['last_name']}"
                print(f"      • {name} - {hire['position']} ({hire['department__name']})")
            
            return True
            
        elif response.status_code == 401:
            print("   ❌ Errore 401 - Non autenticato")
            return False
        else:
            print(f"   ❌ Errore {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Errore di connessione: {e}")
        return False

def run():
    setup_django()
    success = test_dashboard_api()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST DASHBOARD API SUPERATO!")
    else:
        print("❌ TEST DASHBOARD API FALLITO!")
    
    return success

if __name__ == "__main__":
    run()
