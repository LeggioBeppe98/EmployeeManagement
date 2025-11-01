from django.db import models

from django.db import models

# Rappresenta il reparto dove lavora un dipendente
class Department(models.Model):
    # Campi base
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Timestamps automatici
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Come appare nell'admin
    def __str__(self):
        return self.name
    
    # Metodo personalizzato
    def budget_status(self):
        if self.budget > 100000:
            return "High"
        elif self.budget > 50000:
            return "Medium"
        else:
            return "Low"

# Rappresenta il dipendente
class Employee(models.Model):
     # Foreign key
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    # Campi base
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField (unique=True)
    phone = models.CharField (max_length=20, blank=True)
    position = models.CharField (max_length=100)
    salary = models.DecimalField (max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    is_active = models.BooleanField (default=True)

    # Campi timestamp
    created_at = models.DateTimeField (auto_now_add=True)
    updated_at = models.DateTimeField (auto_now=True)

   
    # Come appare nell'admin
    def __str__(self):
        return self.first_name + " " + self.last_name
    