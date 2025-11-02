from django.contrib import admin
import csv
from django.http import HttpResponse

from .models import Department, Employee

class EmployeeAdmin(admin.ModelAdmin):
    # COSA VEDO NELLA LISTA?
    list_display = ['first_name', 'last_name', 'email', 'position', 'department', 'salary']
    
    # COME CERCO?
    search_fields = ['first_name', 'last_name', 'email', 'position']
    
    # COME FILTRO?
    list_filter = ['department', 'position', 'is_active']
    
    # ORDINAMENTO
    ordering = ['last_name', 'first_name']

    # COME SONO ORGANIZZATI I CAMPI NEL FORM?
    fieldsets = [
        ('Informazioni Personali', {
            'fields': ['first_name', 'last_name', 'email', 'phone']
        }),
        ('Informazioni Lavorative', {
            'fields': ['department', 'position', 'salary', 'hire_date']
        }),
        ('Stato', {
            'fields': ['is_active'],
            'classes': ['collapse']  # 👈 Si apre/chiude
        }),
    ]

    # AZIONI BATCH
    actions = ['activate_employees', 'deactivate_employees', 'export_to_csv']
    
    def activate_employees(self, request, queryset):
        """Attiva i dipendenti selezionati"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} dipendenti attivati")
    activate_employees.short_description = "Attiva dipendenti selezionati"
    
    def deactivate_employees(self, request, queryset):
        """Disattiva i dipendenti selezionati"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} dipendenti disattivati")
    deactivate_employees.short_description = "Disattiva dipendenti selezionati"

    def export_to_csv(self, request, queryset):
        """Esporta dipendenti selezionati in CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employees.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Nome', 'Cognome', 'Email', 'Posizione', 'Stipendio', 'Dipartimento'])
        
        for employee in queryset:
            writer.writerow([
                employee.first_name,
                employee.last_name, 
                employee.email,
                employee.position,
                employee.salary,
                employee.department.name
            ])
        
        return response
    export_to_csv.short_description = "Esporta selezionati in CSV"

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'budget', 'employee_count']
    
    def employee_count(self, obj):
        return obj.employee_set.count()
    employee_count.short_description = 'Numero Dipendenti'



# Registra CON personalizzazione
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)

