from django.contrib.auth.models import Group, User
from django.db import models

class CustomUser(models.Model):
    # Relación uno a uno con el modelo User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Relación muchos a muchos con el modelo Group
    groups = models.ManyToManyField(Group, related_name='custom_users')
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('blogger', 'Blogger'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='blogger')
    

    # Puedes agregar otros campos que necesites
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username  # O cualquier otro campo que quieras mostrar
