from django.contrib import admin


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

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'budget', 'employee_count']
    
    def employee_count(self, obj):
        return obj.employee_set.count()
    employee_count.short_description = 'Numero Dipendenti'



# Registra CON personalizzazione
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)

