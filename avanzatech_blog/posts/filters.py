import django_filters
from .models import Comment
from django.contrib.auth.models import User

class CommentFilter(django_filters.FilterSet):
    # Filtrar por autor (usuario)
    author = django_filters.CharFilter(field_name="author__username", lookup_expr="icontains", label="Author")

    # Filtrar por contenido del comentario
    content = django_filters.CharFilter(field_name="content", lookup_expr="icontains", label="Content")

    class Meta:
        model = Comment
        fields = ['author', 'content']