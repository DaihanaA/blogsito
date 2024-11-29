from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAuthorOrReadOnly(BasePermission):
    """
    Permiso personalizado que permite que el autor de un post
    realice cambios, pero permite solo lectura a los demás usuarios.
    """
    def has_object_permission(self, request, view, obj):
        # Permite solo lectura (GET, HEAD, OPTIONS) a todos los usuarios
        if request.method in SAFE_METHODS:
            return True

        # Permite modificación solo al autor del post
        return obj.author == request.user
    

class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado para verificar que el usuario es el autor del post
    o un superusuario.
    """
    def has_object_permission(self, request, view, obj):
        # Solo el autor del post o un superusuario puede borrar el post
        return obj.author == request.user or request.user.is_superuser    
