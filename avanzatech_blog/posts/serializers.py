from rest_framework import serializers
from .models import BlogPost, Like, Comment
from django.contrib.auth.models import Group


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
        
        
    def get_likes(self, obj):
        """Obtiene la lista de usuarios que dieron like al post."""
        return obj.likes.values_list('user__username', flat=True)  # Devuelve solo los nombres de usuario
        

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Para mostrar el nombre del usuario
    blog_post = serializers.StringRelatedField()  # Para mostrar el título del post
    
    class Meta:
        model = Like
        fields  = ['id', 'user', 'blog_post']
        

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Devuelve el nombre de usuario (puedes usar otro campo)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # Formato de la fecha
    
    class Meta:
        model = Comment
        fields = ['id', 'blog_post', 'user', 'content', 'created_at']
        read_only_fields = ['blog_post']
        
    def create(self, validated_data):
        post = self.context.get('post')  # Recupera el post desde el contexto
        if not post:
            raise KeyError("Post not found in context")  # Lanza un error si no se encuentra el post
        return Comment.objects.create(blog_post=post, **validated_data)